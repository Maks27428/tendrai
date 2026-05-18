import { useEffect, useRef, useState } from 'react';
import { subscribeTenderStream } from '../api/client';
import type { StreamEvent } from '../api/client';

export function useSSE(tenderId: number | null) {
  const [event, setEvent] = useState<StreamEvent | null>(null);
  const [done, setDone] = useState(false);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!tenderId) return;
    setDone(false);

    esRef.current = subscribeTenderStream(
      tenderId,
      (e) => setEvent(e),
      () => setDone(true),
    );

    return () => {
      esRef.current?.close();
    };
  }, [tenderId]);

  return { event, done };
}
