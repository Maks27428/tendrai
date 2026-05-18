import json
import time
import threading

from django.http import StreamingHttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Tender
from .serializers import TenderListSerializer, TenderDetailSerializer, TenderUploadSerializer
from ai_pipeline.pipeline import process_tender


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
