import xml.etree.ElementTree as ET

class SSML:

    def __init__(self):
        self.speak = ET.Element('speak')

    def append_child(self,parent, childElements):
        if childElements:
            for elem in childElements:
                for child in elem.speak.findall("./"):
                    parent.append(child)

    def whisper(self, text):
        e = ET.SubElement(self.speak, 'amazon:effect', {'name': 'whispered'})
        e.text = text
        return self

    def sentence(self, text, childElements=None):
        e = ET.SubElement(self.speak, 's')
        e.text = text
        self.append_child(e,childElements)
        return self

    def pause(self, duration, unit="s"):
        if type(duration) == int:
            duration = str(duration) + unit
        e = ET.SubElement(self.speak, 'break', {"time": duration})
        return self

    def interjection(self, text):
        e = ET.SubElement(self.speak, 'say-as', {"interpret-as": "interjection"})
        e.text = text
        return self

    def __repr__(self):
        return ET.tostring(self.speak).decode()

    def __str__(self):
        return ET.tostring(self.speak).decode()



if __name__ == '__main__':
    hr = SSML().sentence("SUB HELLO")
    ssml = SSML().sentence("Hallo",subElements=[hr]).whisper("Ich bin dein Vater.").sentence("berrascht?").interjection("jo").sentence(
        "ok")
    print(ssml)


