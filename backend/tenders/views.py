import json
import time
import threading
from pathlib import Path

from django.conf import settings
from django.http import StreamingHttpResponse, FileResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Tender
from .serializers import TenderListSerializer, TenderDetailSerializer, TenderUploadSerializer
from ai_pipeline.pipeline import process_tender
from ai_pipeline.monopoly import check_monopoly, prepare_tender_data


@api_view(['GET'])
def tender_list(request):
    tenders = Tender.objects.all()[:20]
    serializer = TenderListSerializer(tenders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tender_detail(request, pk):
    try:
        tender = Tender.objects.get(pk=pk)
    except Tender.DoesNotExist:
        return Response({'error': 'Тендер не найден'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TenderDetailSerializer(tender)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def tender_upload(request):
    serializer = TenderUploadSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    tender = serializer.save()

    # Start AI pipeline in background thread
    thread = threading.Thread(target=process_tender, args=(tender.id,), daemon=True)
    thread.start()

    return Response(
        TenderDetailSerializer(tender).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
def demo_pdf_list(request):
    seed_dir = Path(settings.BASE_DIR) / 'seed_data' / 'tenders'
    files = []
    if seed_dir.exists():
        for f in sorted(seed_dir.glob('*.pdf')):
            files.append({'name': f.stem.replace('_', ' ').title(), 'filename': f.name})
    return Response(files)


@api_view(['GET'])
def demo_pdf_download(request, filename):
    filepath = Path(settings.BASE_DIR) / 'seed_data' / 'tenders' / filename
    if not filepath.exists() or not filepath.suffix == '.pdf':
        return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf', filename=filename)


@api_view(['POST'])
def monopoly_check(request):
    tender_ids = request.data.get('tender_ids', [])
    if len(tender_ids) < 2:
        return Response(
            {'error': 'Выберите минимум 2 тендера для проверки'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tenders = Tender.objects.filter(id__in=tender_ids, status='completed')
    if tenders.count() < 2:
        return Response(
            {'error': 'Минимум 2 проанализированных тендера'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    tenders_data = [prepare_tender_data(t) for t in tenders]
    result = check_monopoly(tenders_data)
    return Response(result)


def tender_stream(request, pk):
    """SSE endpoint for real-time progress updates."""
    def event_stream():
        prev_status = None
        prev_message = None
        while True:
            try:
                tender = Tender.objects.get(pk=pk)
            except Tender.DoesNotExist:
                yield f"data: {json.dumps({'error': 'not_found'})}\n\n"
                return

            current = {
                'status': tender.status,
                'message': tender.progress_message,
                'title': tender.title,
                'risk_score': tender.risk_score,
                'page_count': tender.page_count,
            }

            if tender.status != prev_status or tender.progress_message != prev_message:
                yield f"data: {json.dumps(current, ensure_ascii=False)}\n\n"
                prev_status = tender.status
                prev_message = tender.progress_message

            if tender.status in ('completed', 'failed'):
                return

            time.sleep(0.5)

    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream',
    )
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response
