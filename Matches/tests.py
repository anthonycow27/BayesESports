import json

from demjson import decode
from django.urls import reverse
from rest_framework.test import APITestCase

from Matches.management.commands.startconsumer import create_or_update_match
from Matches.models import Match


class MessagesProcessingTests(APITestCase):
    def test_when_message1_is_sent_application_exposes_the_correct_object(self):
        message1 = open('Matches/fixtures/message1.json', 'r').read()
        create_or_update_match(decode(message1))

        response = self.client.get(reverse('match-list'))
        result = json.loads(response.content)
        self.assertEqual(Match.objects.all().count(), 1)
        self.assertEqual(result[0], {'id': '1', 'url': 'https://www.source1.org/matches/1/',
                                     'tournament': {'id': 15, 'name': 'Overbayes Season 1'},
                                     'title': {'name': 'overcooked'},
                                     'teams': [{'id': 1, 'name': 'Bayes Esports Team 1'},
                                               {'id': 2, 'name': 'Bayes Team 2'}],
                                     'state': 1, 'bestof': '3',
                                     'scores': [{'id': 1, 'score': None, 'winner': None, 'match': '1', 'team': 1},
                                                {'id': 2, 'score': None, 'winner': None, 'match': '1', 'team': 2}],
                                     'date_start': '2020-01-07T14:30:00Z'})

    def test_when_message2_is_sent_after_message1_application_exposes_the_correct_object(self):
        message1 = open('Matches/fixtures/message1.json', 'r').read()
        create_or_update_match(decode(message1))

        message2 = open('Matches/fixtures/message2.json', 'r').read()
        create_or_update_match(decode(message2))

        response = self.client.get(reverse('match-list'))
        result = json.loads(response.content)
        self.assertEqual(Match.objects.all().count(), 1)
        self.assertEqual(result[0], {'id': '1', 'url': 'https://www.source1.org/matches/1/',
                                     'tournament': {'id': 15, 'name': 'Overbayes Season 1 - Group Stage'},
                                     'title': {'name': 'overcooked'},
                                     'teams': [{'id': 2, 'name': 'Bayes Team 2'}, {'id': 3, 'name': 'Bayes Team 3'}],
                                     'state': 2, 'bestof': '3',
                                     'scores': [{'id': 3, 'score': 2, 'winner': True, 'match': '1', 'team': 2},
                                                {'id': 4, 'score': 0, 'winner': False, 'match': '1', 'team': 3}],
                                     'date_start': '2020-01-07T15:00:00Z'})

    def test_when_message3_is_sent_application_exposes_the_correct_object(self):
        message3 = open('Matches/fixtures/message3.json', 'r').read()
        create_or_update_match(decode(message3))

        response = self.client.get(reverse('match-list'))
        result = json.loads(response.content)
        self.assertEqual(Match.objects.all().count(), 1)
        self.assertEqual(result[0], {'id': '99', 'url': 'https://www.source2.org/matches/99/bayes1-vs-bayes2',
                                     'tournament': {'id': 1, 'name': 'Overbayes Premium Series'},
                                     'title': {'name': 'overcooked'}, 'teams': [{'id': 2, 'name': 'Bayes Team 2'},
                                                                                {'id': 3, 'name': 'Bayes Esports 3 '}],
                                     'state': 1, 'bestof': None,
                                     'scores': [{'id': 1, 'score': 2, 'winner': True, 'match': '99', 'team': 2},
                                                {'id': 2, 'score': 1, 'winner': False, 'match': '99', 'team': 3}],
                                     'date_start': '2020-01-07T15:15:00Z'})

    def test_when_message4_is_sent_application_exposes_the_correct_object(self):
        message4 = open('Matches/fixtures/message4.json', 'r').read()
        create_or_update_match(decode(message4))

        response = self.client.get(reverse('match-list'))
        result = json.loads(response.content)
        self.assertEqual(Match.objects.all().count(), 1)
        self.assertEqual(result[0], {'id': 'bayes1-bayes2-overcooked-season-2-group-stage-lower-bracket-seed12',
                                     'url': 'https://www.source3.org/matches/bayes1-bayes2-overcooked-season-2-group-stage-lower-bracket-seed12',
                                     'tournament': {'id': 1, 'name': 'Overbayes Tournament Series 2'},
                                     'title': {'name': 'overcooked 2'}, 'teams': [{'id': 17, 'name': 'Bayes Team'},
                                                                                  {'id': 18,
                                                                                   'name': 'Bayes Esports Team'}],
                                     'state': 1, 'bestof': None, 'scores': [{'id': 1, 'score': 1, 'winner': True,
                                                                             'match': 'bayes1-bayes2-overcooked-season-2-group-stage-lower-bracket-seed12',
                                                                             'team': 17},
                                                                            {'id': 2, 'score': 0, 'winner': False,
                                                                             'match': 'bayes1-bayes2-overcooked-season-2-group-stage-lower-bracket-seed12',
                                                                             'team': 18}],
                                     'date_start': '2020-01-07T15:00:00Z'})
