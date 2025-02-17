from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from .views import match_post_api
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from .serializers import Matchserializer

# Create your tests here.


class TestMatchPostAPI(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.match_data = {'match_id': 1,
                           'tournament_id': 101,
                           'timestamp': 235235235,
                           'player1_score': 5,
                           'player2_score': 3,
                           'player1_id': 11,
                           'player2_id': 12,
                           'winner_id': 11}
        self.request = self.factory.post('/api/match/', self.match_data, content_type='application/json')
        self.settings_patcher = patch.object(settings, 'STORE_SCORE', new_callable=MagicMock)
        self.mock_storescore = self.settings_patcher.start()
        self.mock_storescore.add_match.return_value = Response(self.match_data, status=status.HTTP_201_CREATED)

    def tearDown(self):
        self.settings_patcher.stop()

    @patch('TestConnection.serializers.Matchserializer')
    def test_match_post_api_valid_data(self, mock_serializer_class):
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = True
        mock_serializer_instance.validated_data = self.match_data
        mock_serializer_class.return_value = mock_serializer_instance

        response = match_post_api(self.request)
        self.mock_storescore.add_match.assert_called_once_with(self.match_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('TestConnection.serializers.Matchserializer')
    def test_match_post_api_invalid_data(self, mock_serializer_class):
        mock_serializer_instance = MagicMock()
        mock_serializer_instance.is_valid.return_value = False
        mock_serializer_instance.errors = {'match_id': ['A valid integer is required.']}
        mock_serializer_class.return_value = mock_serializer_instance

        response = match_post_api(self.request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'match_id': ['A valid integer is required.']})


class TestMatchSerializer(TestCase):
    def Serializer_valid_match_data(self):
        # Données valides
        valid_data = {
            'match_id': 1,
            'tournament_id': 101,
            'timestamp': 1234567890,
            'player1_score': 5,
            'player2_score': 3,
            'player1_id': 11,
            'player2_id': 12,
            'winner_id': 11
        }
        serializer = Matchserializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, valid_data)

    def Serializer_invalid_match_data(self):
        # Données invalides
        invalid_data = {
            'match_id': 'one',
            'tournament_id': 101,
            'timestamp': 'yesterday',
            'player1_score': -1,
            'player2_score': 3,
            'player1_id': 11,
            'player2_id': 12,
            'winner_id': 11
        }
        serializer = Matchserializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('match_id', serializer.errors)
        self.assertIn('timestamp', serializer.errors)
        self.assertIn('player1_score', serializer.errors)
