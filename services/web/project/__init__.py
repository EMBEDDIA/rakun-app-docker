import os
import json

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)

from flask_restx import Api, Resource, fields, abort, reqparse
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix

from . import api_functions
import stopwordsiso as stopwords
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0',
          title='API services',
          description='RaKUn keyword extractor REST API')
ns = api.namespace('rest_api', description='REST services API')

args = {"distance_threshold":2,
        "distance_method": "editdistance",
        "num_keywords" : 30,
        "pair_diff_length":2,
        "stopwords" : stopwords.stopwords(stopwords.langs()),
        "bigram_count_threshold":2,
        "num_tokens":[1, 2, 3],
	"max_similar" : 3, ## n most similar can show up n times
	"max_occurrence" : 3} ## maximum frequency overall

kw_extractor_input = api.model('KeywordExtractorInput', {
    'text': fields.String(required=True, description='Title + lead + body of the article'),
})

kw_extractor_output = api.model('KeywordExtractorOutput', {
    'keywords': fields.List(fields.String, description='Extracted keywords')
})


@ns.route('/extract_keywords/')
class KeywordExtractor(Resource):
    @ns.doc('Extracts keywords with RaKUn from a news article')
    @ns.expect(kw_extractor_input, validate=True)
    @ns.marshal_with(kw_extractor_output)
    def post(self):
        kw_lem = api_functions.extract_keywords(api.payload['text'], args)
        return {"keywords": kw_lem}

@ns.route('/health/')
class Health(Resource):
    @ns.response(200, "successfully fetched health details")
    def get(self):
        return {"status": "running", "message": "Health check successful"}, 200, {}
