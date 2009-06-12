# -*- coding: utf-8 -*-

"""barcode.base

"""
__docformat__ = 'restructuredtext en'

import codecs

from writer.svg import SVGWriter


class Barcode(object):

    default_writer = SVGWriter()

    default_writer_options = {
        'module_width': 0.2,
        'module_height': 15.0,
        'quiet_zone': 6.5,
        'font_size': 8,
        'background': 'white',
        'foreground': 'black',
        'text': u'',
    }

    def to_ascii(self):
        code = self.build()
        for i, line in enumerate(code):
            code[i] = line.replace(u'1', u'X').replace(u'0', u' ')
        return '\n'.join(code)

    def build(self):
        raise NotImplementedError

    def get_fullcode(self):
        """Returns the full code, encoded in the barcode.

        :returns: Full human readable code.
        :rtype: Unicode
        """
        raise NotImplementedError

    def save(self, filename, **kw):
        """Renders the barcode and saves it in `filename`.

        :parameters:
            filename : String
                Filename to save the barcode in.
            kw : Keyword Arguments
                The same as in `self.render`.
        """
        output = self.render(**kw)
        with codecs.open(filename, 'wb', encoding='utf-8') as f:
            f.write(output)

    def render(self, write_text=True, writer_options=None):
        """Renders the barcode using `self.writer`.

        :parameters:
            write_text : Boolean
                Write the EAN-Code number under the barcode.
            writer_options : Dict
                Options for `self.writer`, see writer docs for details.

        :returns: Output of the writers render method.
        """
        options = Barcode.default_writer_options.copy()
        if write_text:
            options['text'] = self.get_fullcode()
        if writer_options is not None:
            options.update(writer_options)
        self.writer.set_options(**options)
        code = self.build()
        return self.writer.render(code)
