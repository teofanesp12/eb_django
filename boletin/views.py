from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from io import BytesIO
import PyPDF2
from datetime import datetime

from .models import BoletinDocumento
# Create your views here.
def getPDF(request):
    response = HttpResponse(content_type ="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=Documento.pdf'
    output = PyPDF2.PdfFileWriter()
    pdf_file = None
    if request.GET:
        documento = get_object_or_404(BoletinDocumento, pk=request.GET.get("id", 0))
        page  = int(request.GET.get("page", 0))
        limit = int(request.GET.get("limit", 2))
        pdf_file = documento.documento_pdf.open('rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)

        limit_antes  = limit
        limit_depois = limit
        if (page-limit)<0:
            limit_antes  = 0
        if (page+limit>read_pdf.getNumPages()):
            limit_depois = 0

        if limit_antes:
            for x in reversed(range(1, limit_antes+1)):
                output.addPage(read_pdf.getPage(page-x))
        output.addPage(read_pdf.getPage(page))
        if limit_depois:
            for x in range(page+1, page+limit_depois+1):
                output.addPage(read_pdf.getPage(x))

    outputStream = BytesIO()
    output.write(outputStream)
    response.write(outputStream.getvalue())
    # Fechamos o arquivo
    if pdf_file:
        pdf_file.close()
    return response

class Doc:
    paginas = []
    doc_id = 0
def search_militar(request):
    context = {}
    if request.POST:
        dt_inicial = datetime.strptime(request.POST.get("dt_inicial", ""), "%d/%m/%Y")
        dt_final   = datetime.strptime(request.POST.get("dt_final", ""), "%d/%m/%Y")
        limit      = request.POST.get("limit", 0)
        txt = request.POST.get("txt", "")

        context['txt'] = txt
        
        # docs = BoletinDocumento.objects.filter(data_inicio__range=[dt_inicial, dt_final]).filter(data_final__lte=dt_final)
        docs = BoletinDocumento.objects.filter(data_final__lte=dt_final)
        context["limit"] = limit
        context["documentos"] = []
        for doc in docs:
            sh = doc.search_text(txt)
            if not sh:
                continue
            dc = Doc()
            dc.doc_id = doc.pk
            dc.paginas = sh
            context["documentos"].append(dc)

        # raise Exception(context["documentos"][0].paginas)

    return render(request, 'list_search_doc.html', context)