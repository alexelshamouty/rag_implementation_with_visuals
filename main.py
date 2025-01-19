import sys
import argparse
from load_embeddings import load_embeddings
from query import query,document_distance,return_results_embeddings,return_all_embeddings,multi_query,generate_ranked_results
from visualise_embeddings import visualise_embeddings
from expand_query import generate_prompts, generate_answers

def main():
    parser = argparse.ArgumentParser(
        description="RAG load and query your documents"
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Availale commands")

    #Loading into chroma
    load_parser = subparsers.add_parser("load", help="Load a file")
    load_parser.add_argument("filename", type=str, help="The name of the file to load")

    # Querying your stuff with an LLM and query expansion
    query_parser = subparsers.add_parser("query", help="Query a string")
    query_parser.add_argument("query_string", type=str, help="The string to query")
    query_parser.add_argument(
        "--visualise",
        action="store_true",
        help="Visualise the query and results embeddings on a graph using UMAP"
    )

    augmentation_parser = subparsers.add_parser("augment", help="Query ChatGPT for expanding your queries")
    augmentation_parser.add_argument("question",type=str, help="The string to query")
    augmentation_parser.add_argument(
        "--visualise",
        action="store_true",
        help="Visualise the query and results embeddings on a graph using UMAP"
        )
    augmentation_parser.add_argument(
        "--restrict",
        action="store_true",
        help="Restrict to top 5 ranked augmented results"
        )
    args = parser.parse_args()

    

    if args.command == "load":
        load_embeddings(args.filename)
    elif args.command == "query":
        results=query(args.query_string)
        for _, distance in document_distance(results):
            print(distance)
        if(args.visualise):
            visualise_embeddings([args.query_string],return_results_embeddings(results),return_all_embeddings())
    elif args.command == 'augment':
        queries = generate_prompts(args.question)
        documents, embeddings, distances = multi_query(queries)
        if(args.visualise):
            #Get the opriginal results embeddings
            results=query(args.question)
            visualise_embeddings([args.question],return_results_embeddings(results),return_all_embeddings(), embeddings)
        if(args.restrict):
            scores, documents = generate_ranked_results(queries)
            attached_documents = []
            questions = [args.question]
            for score, document in zip(scores,documents):
                print(score)
                attached_documents.append(document['document'])
                questions.append(document['query_text'])
            response = generate_answers(args.question, attached_documents)
            print(response.content)

if __name__ == "__main__":
    main()