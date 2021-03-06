# Copyright 2014-2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from synapse.rest.media.v1.preview_url_resource import (
    decode_and_calc_og,
    get_html_media_encoding,
    summarize_paragraphs,
)

from . import unittest

try:
    import lxml
except ImportError:
    lxml = None


class SummarizeTestCase(unittest.TestCase):
    if not lxml:
        skip = "url preview feature requires lxml"

    def test_long_summarize(self):
        example_paras = [
            """Tromsø (Norwegian pronunciation: [ˈtrʊmsœ] ( listen); Northern Sami:
            Romsa; Finnish: Tromssa[2] Kven: Tromssa) is a city and municipality in
            Troms county, Norway. The administrative centre of the municipality is
            the city of Tromsø. Outside of Norway, Tromso and Tromsö are
            alternative spellings of the city.Tromsø is considered the northernmost
            city in the world with a population above 50,000. The most populous town
            north of it is Alta, Norway, with a population of 14,272 (2013).""",
            """Tromsø lies in Northern Norway. The municipality has a population of
            (2015) 72,066, but with an annual influx of students it has over 75,000
            most of the year. It is the largest urban area in Northern Norway and the
            third largest north of the Arctic Circle (following Murmansk and Norilsk).
            Most of Tromsø, including the city centre, is located on the island of
            Tromsøya, 350 kilometres (217 mi) north of the Arctic Circle. In 2012,
            Tromsøya had a population of 36,088. Substantial parts of the urban area
            are also situated on the mainland to the east, and on parts of Kvaløya—a
            large island to the west. Tromsøya is connected to the mainland by the Tromsø
            Bridge and the Tromsøysund Tunnel, and to the island of Kvaløya by the
            Sandnessund Bridge. Tromsø Airport connects the city to many destinations
            in Europe. The city is warmer than most other places located on the same
            latitude, due to the warming effect of the Gulf Stream.""",
            """The city centre of Tromsø contains the highest number of old wooden
            houses in Northern Norway, the oldest house dating from 1789. The Arctic
            Cathedral, a modern church from 1965, is probably the most famous landmark
            in Tromsø. The city is a cultural centre for its region, with several
            festivals taking place in the summer. Some of Norway's best-known
             musicians, Torbjørn Brundtland and Svein Berge of the electronica duo
             Röyksopp and Lene Marlin grew up and started their careers in Tromsø.
             Noted electronic musician Geir Jenssen also hails from Tromsø.""",
        ]

        desc = summarize_paragraphs(example_paras, min_size=200, max_size=500)

        self.assertEqual(
            desc,
            "Tromsø (Norwegian pronunciation: [ˈtrʊmsœ] ( listen); Northern Sami:"
            " Romsa; Finnish: Tromssa[2] Kven: Tromssa) is a city and municipality in"
            " Troms county, Norway. The administrative centre of the municipality is"
            " the city of Tromsø. Outside of Norway, Tromso and Tromsö are"
            " alternative spellings of the city.Tromsø is considered the northernmost"
            " city in the world with a population above 50,000. The most populous town"
            " north of it is Alta, Norway, with a population of 14,272 (2013).",
        )

        desc = summarize_paragraphs(example_paras[1:], min_size=200, max_size=500)

        self.assertEqual(
            desc,
            "Tromsø lies in Northern Norway. The municipality has a population of"
            " (2015) 72,066, but with an annual influx of students it has over 75,000"
            " most of the year. It is the largest urban area in Northern Norway and the"
            " third largest north of the Arctic Circle (following Murmansk and Norilsk)."
            " Most of Tromsø, including the city centre, is located on the island of"
            " Tromsøya, 350 kilometres (217 mi) north of the Arctic Circle. In 2012,"
            " Tromsøya had a population of 36,088. Substantial parts of the urban…",
        )

    def test_short_summarize(self):
        example_paras = [
            "Tromsø (Norwegian pronunciation: [ˈtrʊmsœ] ( listen); Northern Sami:"
            " Romsa; Finnish: Tromssa[2] Kven: Tromssa) is a city and municipality in"
            " Troms county, Norway.",
            "Tromsø lies in Northern Norway. The municipality has a population of"
            " (2015) 72,066, but with an annual influx of students it has over 75,000"
            " most of the year.",
            "The city centre of Tromsø contains the highest number of old wooden"
            " houses in Northern Norway, the oldest house dating from 1789. The Arctic"
            " Cathedral, a modern church from 1965, is probably the most famous landmark"
            " in Tromsø.",
        ]

        desc = summarize_paragraphs(example_paras, min_size=200, max_size=500)

        self.assertEqual(
            desc,
            "Tromsø (Norwegian pronunciation: [ˈtrʊmsœ] ( listen); Northern Sami:"
            " Romsa; Finnish: Tromssa[2] Kven: Tromssa) is a city and municipality in"
            " Troms county, Norway.\n"
            "\n"
            "Tromsø lies in Northern Norway. The municipality has a population of"
            " (2015) 72,066, but with an annual influx of students it has over 75,000"
            " most of the year.",
        )

    def test_small_then_large_summarize(self):
        example_paras = [
            "Tromsø (Norwegian pronunciation: [ˈtrʊmsœ] ( listen); Northern Sami:"
            " Romsa; Finnish: Tromssa[2] Kven: Tromssa) is a city and municipality in"
            " Troms county, Norway.",
            "Tromsø lies in Northern Norway. The municipality has a population of"
            " (2015) 72,066, but with an annual influx of students it has over 75,000"
            " most of the year."
            " The city centre of Tromsø contains the highest number of old wooden"
            " houses in Northern Norway, the oldest house dating from 1789. The Arctic"
            " Cathedral, a modern church from 1965, is probably the most famous landmark"
            " in Tromsø.",
        ]

        desc = summarize_paragraphs(example_paras, min_size=200, max_size=500)
        self.assertEqual(
            desc,
            "Tromsø (Norwegian pronunciation: [ˈtrʊmsœ] ( listen); Northern Sami:"
            " Romsa; Finnish: Tromssa[2] Kven: Tromssa) is a city and municipality in"
            " Troms county, Norway.\n"
            "\n"
            "Tromsø lies in Northern Norway. The municipality has a population of"
            " (2015) 72,066, but with an annual influx of students it has over 75,000"
            " most of the year. The city centre of Tromsø contains the highest number"
            " of old wooden houses in Northern Norway, the oldest house dating from"
            " 1789. The Arctic Cathedral, a modern church from…",
        )


class CalcOgTestCase(unittest.TestCase):
    if not lxml:
        skip = "url preview feature requires lxml"

    def test_simple(self):
        html = b"""
        <html>
        <head><title>Foo</title></head>
        <body>
        Some text.
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(og, {"og:title": "Foo", "og:description": "Some text."})

    def test_comment(self):
        html = b"""
        <html>
        <head><title>Foo</title></head>
        <body>
        <!-- HTML comment -->
        Some text.
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(og, {"og:title": "Foo", "og:description": "Some text."})

    def test_comment2(self):
        html = b"""
        <html>
        <head><title>Foo</title></head>
        <body>
        Some text.
        <!-- HTML comment -->
        Some more text.
        <p>Text</p>
        More text
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(
            og,
            {
                "og:title": "Foo",
                "og:description": "Some text.\n\nSome more text.\n\nText\n\nMore text",
            },
        )

    def test_script(self):
        html = b"""
        <html>
        <head><title>Foo</title></head>
        <body>
        <script> (function() {})() </script>
        Some text.
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(og, {"og:title": "Foo", "og:description": "Some text."})

    def test_missing_title(self):
        html = b"""
        <html>
        <body>
        Some text.
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(og, {"og:title": None, "og:description": "Some text."})

    def test_h1_as_title(self):
        html = b"""
        <html>
        <meta property="og:description" content="Some text."/>
        <body>
        <h1>Title</h1>
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(og, {"og:title": "Title", "og:description": "Some text."})

    def test_missing_title_and_broken_h1(self):
        html = b"""
        <html>
        <body>
        <h1><a href="foo"/></h1>
        Some text.
        </body>
        </html>
        """

        og = decode_and_calc_og(html, "http://example.com/test.html")

        self.assertEqual(og, {"og:title": None, "og:description": "Some text."})

    def test_empty(self):
        """Test a body with no data in it."""
        html = b""
        og = decode_and_calc_og(html, "http://example.com/test.html")
        self.assertEqual(og, {})

    def test_no_tree(self):
        """A valid body with no tree in it."""
        html = b"\x00"
        og = decode_and_calc_og(html, "http://example.com/test.html")
        self.assertEqual(og, {})

    def test_invalid_encoding(self):
        """An invalid character encoding should be ignored and treated as UTF-8, if possible."""
        html = b"""
        <html>
        <head><title>Foo</title></head>
        <body>
        Some text.
        </body>
        </html>
        """
        og = decode_and_calc_og(
            html, "http://example.com/test.html", "invalid-encoding"
        )
        self.assertEqual(og, {"og:title": "Foo", "og:description": "Some text."})

    def test_invalid_encoding2(self):
        """A body which doesn't match the sent character encoding."""
        # Note that this contains an invalid UTF-8 sequence in the title.
        html = b"""
        <html>
        <head><title>\xff\xff Foo</title></head>
        <body>
        Some text.
        </body>
        </html>
        """
        og = decode_and_calc_og(html, "http://example.com/test.html")
        self.assertEqual(og, {"og:title": "ÿÿ Foo", "og:description": "Some text."})


class MediaEncodingTestCase(unittest.TestCase):
    def test_meta_charset(self):
        """A character encoding is found via the meta tag."""
        encoding = get_html_media_encoding(
            b"""
        <html>
        <head><meta charset="ascii">
        </head>
        </html>
        """,
            "text/html",
        )
        self.assertEqual(encoding, "ascii")

        # A less well-formed version.
        encoding = get_html_media_encoding(
            b"""
        <html>
        <head>< meta charset = ascii>
        </head>
        </html>
        """,
            "text/html",
        )
        self.assertEqual(encoding, "ascii")

    def test_meta_charset_underscores(self):
        """A character encoding contains underscore."""
        encoding = get_html_media_encoding(
            b"""
        <html>
        <head><meta charset="Shift_JIS">
        </head>
        </html>
        """,
            "text/html",
        )
        self.assertEqual(encoding, "Shift_JIS")

    def test_xml_encoding(self):
        """A character encoding is found via the meta tag."""
        encoding = get_html_media_encoding(
            b"""
        <?xml version="1.0" encoding="ascii"?>
        <html>
        </html>
        """,
            "text/html",
        )
        self.assertEqual(encoding, "ascii")

    def test_meta_xml_encoding(self):
        """Meta tags take precedence over XML encoding."""
        encoding = get_html_media_encoding(
            b"""
        <?xml version="1.0" encoding="ascii"?>
        <html>
        <head><meta charset="UTF-16">
        </head>
        </html>
        """,
            "text/html",
        )
        self.assertEqual(encoding, "UTF-16")

    def test_content_type(self):
        """A character encoding is found via the Content-Type header."""
        # Test a few variations of the header.
        headers = (
            'text/html; charset="ascii";',
            "text/html;charset=ascii;",
            'text/html;  charset="ascii"',
            "text/html; charset=ascii",
            'text/html; charset="ascii;',
            'text/html; charset=ascii";',
        )
        for header in headers:
            encoding = get_html_media_encoding(b"", header)
            self.assertEqual(encoding, "ascii")

    def test_fallback(self):
        """A character encoding cannot be found in the body or header."""
        encoding = get_html_media_encoding(b"", "text/html")
        self.assertEqual(encoding, "utf-8")
