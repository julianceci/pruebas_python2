#Para ejecuctarlas sólo hay que correr pytest desde la base del proyecto y esto busca las def con prefijo test_ y las corre
from my_package import Document

def test_document_tokens():
    doc = Document("a e i o u")
    
    #assert doc.tokens == ["a", "e", "i", "o", "u"]
    assert doc.text == "a e i o u"

def test_document_tokens_empty():
    doc = Document("")
    
    #assert doc.tokens == [""]
    assert doc.text == ""