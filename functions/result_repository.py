from google.cloud import firestore
from result import Result, Date, Team


class ResultReposiroty:
    def __init__(self):
        db = firestore.Client()
        self.collection = db.collection('result')

    def save(self, result: Result):
        self.collection.add(result.to_dict())

    def update(self, result: Result):
        doc_id = self.collection.where(u'date', u'==', result.date).where(
            u'team', u'==', result.team).get()[0].id
        self.collection.document(doc_id).update({u'content.record.texts': result.to_dict()
                                                 [u'content'][u'record'][u'texts']})

    def find(self,  date: Date, team: Team):
        docs = self.collection.where(u'date', u'==', date).where(
            u'team', u'==', team).get()
        return docs
