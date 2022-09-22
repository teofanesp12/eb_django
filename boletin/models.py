from django.db import models

import PyPDF2, re

# Create your models here.
class TipoBoletin(models.Model):
    nome   = models.CharField(max_length=250)
    abreviacao = models.CharField(max_length=100)
    def __str__(self):
        return self.nome or ""

def file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'doc_{0}/{1}:{2}.pdf'.format(instance.tipo.abreviacao, instance.data_inicio.strftime('%d-%m-%Y'), instance.data_final.strftime('%d-%m-%Y'))

class BoletinDocumento(models.Model):
    nome            = models.CharField(max_length=200, help_text="BI, BAR ou ADT. (anual ou semestral)", null=True)
    data_inicio     = models.DateField()
    data_final      = models.DateField()
    tipo            = models.ForeignKey(TipoBoletin, on_delete=models.CASCADE)
    documento_pdf   = models.FileField(upload_to=file_directory_path)

    def search_text(self, txt):
        pdf_file = self.documento_pdf.open('rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        # number_of_pages = read_pdf.getNumPages()
        page_include = []
        for count in range(0,read_pdf.getNumPages()):
            page = read_pdf.getPage(count)
            page_content = page.extractText()
            parsed = page_content.replace('\n','')
            if re.search(txt, parsed):# parsed != (parsed.replace(txt, '')):
                page_include.append(count)
            # raise Exception(parsed)
        pdf_file.close()
        return page_include

    def __str__(self):
        return 'doc_{0}/{1}:{2}.pdf'.format(self.tipo.abreviacao, self.data_inicio.strftime('%d-%m-%Y'), self.data_final.strftime('%d-%m-%Y'))

    class Meta:
        ordering = ['tipo', 'data_final']