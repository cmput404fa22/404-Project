from django import template
from django.template.defaultfilters import stringfilter
import cmarkgfm

############################################################################
# Python binding to Commonmark provided by cmarkgfm module
#   Documentation can be found at https://github.com/theacodes/cmarkgfm
#   License states permission for commercial and private use
############################################################################

register = template.Library()

@register.filter()
@stringfilter
def markdown(content):
    return cmarkgfm.markdown_to_html(content)