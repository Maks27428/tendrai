from django.db import models


class Tender(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Загружен'),
        ('parsing', 'Парсинг PDF'),
        ('extracting', 'Извлечение требований'),
        ('scoring', 'Оценка рисков'),
        ('generating', 'Генерация предложения'),
        ('completed', 'Завершён'),
        ('failed', 'Ошибка'),
    ]

    title = models.CharField(max_length=500, blank=True)
    pdf_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    progress_message = models.CharField(max_length=200, blank=True)

    parsed_text = models.TextField(blank=True)
    page_count = models.IntegerField(null=True)
    summary = models.JSONField(null=True, blank=True)
    risk_score = models.IntegerField(null=True)
    risk_explanation = models.TextField(blank=True)
    pitfalls = models.JSONField(null=True, blank=True)
    contacts = models.JSONField(null=True, blank=True)

    technical_proposal = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f'Тендер #{self.pk}'


class Requirement(models.Model):
    CATEGORY_CHOICES = [
        ('qualification', 'Квалификация'),
        ('technical', 'Технические'),
        ('financial', 'Финансовые'),
        ('deadline', 'Сроки'),
        ('document', 'Документы'),
    ]
    STATUS_CHOICES = [
        ('needs_review', 'Требует проверки'),
        ('critical', 'Критично'),
        ('warning', 'Предупреждение'),
        ('ok', 'Соответствует'),
    ]

    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='requirements')
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='needs_review')
    details = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.get_category_display()}: {self.text[:80]}'
