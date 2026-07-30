import unittest

from app.models.schema import MaterialInfo
from app.services import script_materials


class TestScriptMaterials(unittest.TestCase):
    def test_split_script_segments_uses_sentences_for_single_paragraph(self):
        script = (
            "Comece com um gancho forte. "
            "O Gamma cria apresentações. "
            "O Claude analisa documentos? "
            "O CapCut edita vídeos!"
        )

        self.assertEqual(
            script_materials.split_script_segments(script),
            [
                "Comece com um gancho forte.",
                "O Gamma cria apresentações.",
                "O Claude analisa documentos?",
                "O CapCut edita vídeos!",
            ],
        )

    def test_split_script_segments_preserves_explicit_paragraphs(self):
        script = "Introdução com duas frases. Ainda é a introdução.\n\nParte do Gamma."

        self.assertEqual(
            script_materials.split_script_segments(script),
            [
                "Introdução com duas frases. Ainda é a introdução.",
                "Parte do Gamma.",
            ],
        )

    def test_order_materials_by_segment_is_stable_and_keeps_fallbacks(self):
        materials = [
            MaterialInfo(provider="local", url="fallback.mp4"),
            MaterialInfo(provider="local", url="capcut.mp4", segment_index=3),
            MaterialInfo(provider="local", url="gamma-1.png", segment_index=1),
            MaterialInfo(provider="local", url="gamma-2.mp4", segment_index=1),
            MaterialInfo(provider="local", url="claude.png", segment_index=2),
        ]

        ordered = script_materials.order_materials_by_segment(materials)

        self.assertEqual(
            [material.url for material in ordered],
            [
                "gamma-1.png",
                "gamma-2.mp4",
                "claude.png",
                "capcut.mp4",
                "fallback.mp4",
            ],
        )

    def test_order_materials_without_assignments_preserves_upload_order(self):
        materials = [
            MaterialInfo(provider="local", url="first.png"),
            MaterialInfo(provider="local", url="second.png"),
        ]

        self.assertEqual(
            script_materials.order_materials_by_segment(materials),
            materials,
        )

    def test_has_segment_assignments_distinguishes_ordered_materials(self):
        self.assertFalse(
            script_materials.has_segment_assignments(
                [MaterialInfo(provider="local", url="fallback.png")]
            )
        )
        self.assertTrue(
            script_materials.has_segment_assignments(
                [
                    MaterialInfo(provider="local", url="fallback.png"),
                    MaterialInfo(
                        provider="local",
                        url="gamma.png",
                        segment_index=0,
                    ),
                ]
            )
        )


if __name__ == "__main__":
    unittest.main()
