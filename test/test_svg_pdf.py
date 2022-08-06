from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPDF
import xml.dom.minidom
@csrf_exempt
def export_svg(request):
    # Get data from client side via POST variables
    svg = request.POST.get("svg")
    doc = xml.dom.minidom.parseString(svg.encode( "utf-8" ))
    svg = doc.documentElement
    # Create new instance of SvgRenderer class
    svgRenderer = SvgRenderer()
    svgRenderer.render(svg)
    drawing = svgRenderer.finish()

    # Instead of outputting to a file, we simple return
    # the data and let the user download to their machine
    pdf = renderPDF.drawToString(drawing)
    response = HttpResponse(mimetype='application/pdf')
    response.write(pdf)     

    # If one were to remove the 'attachment; ' from this line
    # it would simple invoke the browsers default PDF plugin
    response["Content-Disposition"]= "attachment; filename=converted.pdf"
    return response