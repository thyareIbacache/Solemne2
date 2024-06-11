from flask import Blueprint, request, jsonify
import whoosh.index as index
from whoosh.qparser import QueryParser

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    ix = index.open_dir("indexdir")
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(query)
    with ix.searcher() as s:
        results = s.search(q)
        return jsonify([dict(result) for result in results])
