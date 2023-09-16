import grpc
import text_summarizer_pb2
import text_summarizer_pb2_grpc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from concurrent import futures 
class TextSummarizerServicer(text_summarizer_pb2_grpc.TextSummarizerServicer):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

    def Summarize(self, request, context):
        input_text = request.text
        max_length = request.max_length

        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = self.model.generate(inputs["input_ids"], max_length=max_length, num_beams=4, length_penalty=2.0, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return text_summarizer_pb2.SummarizeResponse(summary=summary)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_summarizer_pb2_grpc.add_TextSummarizerServicer_to_server(TextSummarizerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
