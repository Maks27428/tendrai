import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export interface TenderSummary {
  amount: string;
  deadline: string;
  customer: string;
  category: string;
  delivery_location: string;
}

export interface RequirementData {
  id: number;
  text: string;
  category: string;
  status: string;
  details: string;
  order: number;
}

export interface Pitfall {
  text: string;
  severity: string;
  recommendation?: string;
}

export interface TenderDetail {
  id: number;
  title: string;
  status: string;
  progress_message: string;
  page_count: number | null;
  summary: TenderSummary | null;
  risk_score: number | null;
  risk_explanation: string;
  pitfalls: Pitfall[] | null;
  technical_proposal: string;
  requirements: RequirementData[];
  created_at: string;
  updated_at: string;
}

export interface TenderListItem {
  id: number;
  title: string;
  status: string;
  risk_score: number | null;
  page_count: number | null;
  created_at: string;
  summary?: TenderSummary | null;
  requirements_count?: number | null;
}

export interface StreamEvent {
  status: string;
  message: string;
  title?: string;
  risk_score?: number | null;
  page_count?: number | null;
  error?: string;
}

export interface DemoPdf {
  name: string;
  filename: string;
}

export async function getDemoPdfs(): Promise<DemoPdf[]> {
  const { data } = await api.get<DemoPdf[]>('/tenders/demo-pdfs/');
  return data;
}

export async function uploadDemoPdf(filename: string): Promise<TenderDetail> {
  const response = await api.get(`/tenders/demo-pdfs/${filename}/`, { responseType: 'blob' });
  const file = new File([response.data], filename, { type: 'application/pdf' });
  return uploadTender(file);
}

export async function uploadTender(file: File): Promise<TenderDetail> {
  const formData = new FormData();
  formData.append('pdf_file', file);
  const { data } = await api.post<TenderDetail>('/tenders/upload/', formData);
  return data;
}

export async function getTender(id: number): Promise<TenderDetail> {
  const { data } = await api.get<TenderDetail>(`/tenders/${id}/`);
  return data;
}

export async function getTenders(): Promise<TenderListItem[]> {
  const { data } = await api.get<TenderListItem[]>('/tenders/');
  return data;
}

export interface MonopolyFlag {
  type: string;
  severity: string;
  description: string;
  tenders_involved: number[];
  evidence: string;
}

export interface MonopolyResult {
  monopoly_score: number;
  verdict: 'clean' | 'suspicious' | 'critical';
  summary: string;
  flags: MonopolyFlag[];
  recommendations: string[];
}

export async function checkMonopoly(tenderIds: number[]): Promise<MonopolyResult> {
  const { data } = await api.post<MonopolyResult>('/tenders/monopoly-check/', {
    tender_ids: tenderIds,
  });
  return data;
}

export function subscribeTenderStream(
  id: number,
  onEvent: (event: StreamEvent) => void,
  onDone: () => void,
): EventSource {
  const es = new EventSource(`/api/tenders/${id}/stream/`);
  es.onmessage = (e) => {
    const data: StreamEvent = JSON.parse(e.data);
    onEvent(data);
    if (data.status === 'completed' || data.status === 'failed' || data.error) {
      es.close();
      onDone();
    }
  };
  es.onerror = () => {
    es.close();
    onDone();
  };
  return es;
}
