from google.cloud import documentai_v1beta2 as documentai
from google.oauth2 import service_account #Control API Keys

keyDIR = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-documentAI.json"

credentials = service_account.Credentials.from_service_account_file(keyDIR) #using service account to go through google
client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)

gcs_source = documentai.types.GcsSource(uri="gs://document_ai_resume/Document_0.pdf")

# mime_type can be application/pdf, image/tiff,
# and image/gif, or application/json
input_config = documentai.types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')

# Improve form parsing results by providing key-value pair hints.
# For each key hint, key is text that is likely to appear in the
# document as a form field name (i.e. "DOB").
# Value types are optional, but can be one or more of:
# ADDRESS, LOCATION, ORGANIZATION, PERSON, PHONE_NUMBER, ID,
# NUMBER, EMAIL, PRICE, TERMS, DATE, NAME
key_value_pair_hints = [
    documentai.types.KeyValuePairHint(key='Emergency Contact',value_types=['NAME']),
    documentai.types.KeyValuePairHint(key='Referred By')
]

# Setting enabled=True enables form extraction
form_extraction_params = documentai.types.FormExtractionParams(
    enabled=True, key_value_pair_hints=key_value_pair_hints)

# Location can be 'us' or 'eu'
parent = 'projects/{}/locations/us'.format("resumematcher")
request = documentai.types.ProcessDocumentRequest(
    parent=parent,
    input_config=input_config,
    form_extraction_params=form_extraction_params)

document = client.process_document(request=request)
#print(document)
def _get_text(el):
    """Doc AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ''
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in el.text_anchor.text_segments:
        start_index = segment.start_index
        end_index = segment.end_index
        response += document.text[start_index:end_index]
    return response

for page in document.pages:
    print('Page number: {}'.format(page.page_number))
    for form_field in page.form_fields:
        print('Field Name: {}\tConfidence: {}'.format(
            _get_text(form_field.field_name),
            form_field.field_name.confidence))
        print('Field Value: {}\tConfidence: {}'.format(
            _get_text(form_field.field_value),
            form_field.field_value.confidence))

print("----------------------------------------------------------------------------------------------------------------------------------------------------------")
# mime_type can be application/pdf, image/tiff,
# and image/gif, or application/json
input_config = documentai.types.InputConfig(
    gcs_source=gcs_source, mime_type='application/pdf')

# Improve table parsing results by providing bounding boxes
# specifying where the box appears in the document (optional)
table_bound_hints = [
    documentai.types.TableBoundHint(
        page_number=1,
        bounding_box=documentai.types.BoundingPoly(
            # Define a polygon around tables to detect
            # Each vertice coordinate must be a number between 0 and 1
            normalized_vertices=[
                # Top left
                documentai.types.geometry.NormalizedVertex(
                    x=0,
                    y=0
                ),
                # Top right
                documentai.types.geometry.NormalizedVertex(
                    x=1,
                    y=0
                ),
                # Bottom right
                documentai.types.geometry.NormalizedVertex(
                    x=1,
                    y=1
                ),
                # Bottom left
                documentai.types.geometry.NormalizedVertex(
                    x=0,
                    y=1
                )
            ]
        )
    )
]

# Setting enabled=True enables form extraction
table_extraction_params = documentai.types.TableExtractionParams(
    enabled=True, table_bound_hints=table_bound_hints)

# Location can be 'us' or 'eu'
parent = 'projects/{}/locations/us'.format("resumematcher")
request = documentai.types.ProcessDocumentRequest(
    parent=parent,
    input_config=input_config,
    table_extraction_params=table_extraction_params)

document = client.process_document(request=request)

def _get_text(el):
    """Convert text offset indexes into text snippets.
    """
    response = ''
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in el.text_anchor.text_segments:
        start_index = segment.start_index
        end_index = segment.end_index
        response += document.text[start_index:end_index]
    return response

for page in document.pages:
    print('Page number: {}'.format(page.page_number))
    for table_num, table in enumerate(page.tables):
        print('Table {}: '.format(table_num))
        for row_num, row in enumerate(table.header_rows):
            cells = '\t'.join(
                [_get_text(cell.layout) for cell in row.cells])
            print('Header Row {}: {}'.format(row_num, cells))
        for row_num, row in enumerate(table.body_rows):
            cells = '\t'.join(
                [_get_text(cell.layout) for cell in row.cells])
            print('Row {}: {}'.format(row_num, cells))