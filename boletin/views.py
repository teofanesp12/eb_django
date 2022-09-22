from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from io import BytesIO
import PyPDF2
from datetime import datetime

from .models import BoletinDocumento
# Create your views here.
@login_required
def getPDF(request):
    response = HttpResponse(content_type ="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=Documento.pdf'
    output = PyPDF2.PdfFileWriter()
    pdf_file = None
    if request.GET:
        documento = get_object_or_404(BoletinDocumento, pk=request.GET.get("id", 0))
        page  = int(request.GET.get("page", 0))
        limit = int(request.GET.get("limit", 2) or 2)
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
    doc_id  = 0
    nome = ""
def search_militar(request):
    context = {}
    if request.POST:
        # dt_inicial = datetime.strptime(request.POST.get("dt_inicial", ""), "%d/%m/%Y")
        # dt_final   = datetime.strptime(request.POST.get("dt_final", ""), "%d/%m/%Y")
        # docs = BoletinDocumento.objects.filter(data_inicio__range=[dt_inicial, dt_final]).filter(data_final__lte=dt_final)
        # docs = BoletinDocumento.objects.filter(data_final__lte=dt_final)
        limit = request.POST.get("limit", 0)
        txt   = request.POST.get("txt", "")
        bols  = request.POST.getlist('bol[]')
        docs  = []
        for bol in bols:
            docs.append(int(bol))

        context['txt'] = txt
        context["limit"] = limit
        context["documentos"] = []
        for doc in BoletinDocumento.objects.filter(pk__in=docs):
            sh = doc.search_text(txt)
            if not sh:
                continue
            dc = Doc()
            dc.doc_id  = doc.pk
            dc.paginas = sh
            dc.nome    = doc.nome
            context["documentos"].append(dc)

        # raise Exception(context["documentos"][0].paginas)
        # raise Exception(docs)

    return render(request, 'list_search_doc.html', context)