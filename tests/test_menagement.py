import unittest
from menagement import classify

class TestClassification(unittest.TestCase):
    def test_brief(self): self.assertEqual(classify('hey').level, 1)
    def test_question(self): self.assertEqual(classify('How was your weekend?').level, 2)
    def test_thoughtful(self): self.assertEqual(classify('I noticed your interest in art and I appreciate how you describe your work because it sounds creative. What kind of project are you most excited about right now?').level, 3)
    def test_boundary(self): self.assertEqual(classify('send nudes').level, 0)
    def test_empty(self):
        with self.assertRaises(ValueError): classify('   ')
    def test_three_suggestions(self): self.assertEqual(len(classify('hello').suggestions), 3)
    def test_human_review(self): self.assertTrue(classify('hello').review_required)

if __name__ == '__main__': unittest.main()
