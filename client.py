import grpc
import text_summarizer_pb2
import text_summarizer_pb2_grpc

def summarize_text(text, max_length):
    channel = grpc.insecure_channel('localhost:50051')
    stub = text_summarizer_pb2_grpc.TextSummarizerStub(channel)
    
    request = text_summarizer_pb2.SummarizeRequest(text=text, max_length=max_length)
    response = stub.Summarize(request)
    
    return response.summary

if __name__ == '__main__':
    text = "Once upon a time, in a land far, far away, there was a brave knight named Sir Lancelot. Sir Lancelot embarked on a quest to rescue the princess from the clutches of the evil dragon. Armed with his trusty sword, he journeyed through dark forests and treacherous mountains, facing many challenges along the way. After a long and perilous journey, Sir Lancelot finally confronted the dragon in a fierce battle. With great courage and skill, he defeated the dragon and rescued the princess, bringing peace and happiness to the kingdom."
    max_length = 150
    
    summary = summarize_text(text, max_length)
    print("Summary:", summary)
