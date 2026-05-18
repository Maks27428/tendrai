import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText } from 'lucide-react';

interface Props {
  onUpload: (file: File) => void;
  isUploading: boolean;
}

export default function UploadZone({ onUpload, isUploading }: Props) {
  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted.length > 0) onUpload(accepted[0]);
    },
    [onUpload],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxSize: 52428800,
    multiple: false,
    disabled: isUploading,
  });

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer
        transition-all duration-300
        ${isDragActive ? 'border-primary bg-primary/10 scale-[1.02]' : 'border-border hover:border-primary/50 hover:bg-surface-2'}
        ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-4">
        {isUploading ? (
          <>
            <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="text-lg text-text">Загружаем документ...</p>
          </>
        ) : isDragActive ? (
          <>
            <FileText className="w-16 h-16 text-primary" />
            <p className="text-lg text-primary font-medium">Отпустите файл</p>
          </>
        ) : (
          <>
            <Upload className="w-16 h-16 text-text-muted" />
            <div>
              <p className="text-lg text-text font-medium">
                Перетащите PDF тендера сюда
              </p>
              <p className="text-sm text-text-muted mt-2">
                или нажмите для выбора файла (макс. 50 МБ)
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
