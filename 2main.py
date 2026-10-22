import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field

# 1. ვტვირთავთ გარემოს ცვლადებს
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. ვსაზღვრავთ Pydantic მოდელს სტრუქტურირებული პასუხისთვის
class ProductReviewEvaluation(BaseModel):
    sentiment: str = Field(
        description="შეფასების განწყობა: უნდა იყოს ზუსტად ერთ-ერთი ამ სამიდან: positive, negative, ან neutral."
    )
    pros: list[str] = Field(
        description="პროდუქტის დადებითი მხარეები (სტრიქონების სია)."
    )
    cons: list[str] = Field(
        description="პროდუქტის უარყოფითი მხარეები (სტრიქონების სია)."
    )
    summary: str = Field(
        description="მიმოხილვის მოკლე შეჯამება."
    )
    recommend: bool = Field(
        description="ურჩევს თუ არა მომხმარებელს ამ პროდუქტის შეძენას (True ან False)."
    )

def evaluate_review(review_text: str):
    # ვიყენებთ ზუსტად იმ მოდელს, რომელიც სიიდან ამოვიდა
    model = genai.GenerativeModel(
        model_name='gemini-3.5-flash',
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": ProductReviewEvaluation,
            "temperature": 0.2
        }
    )

    prompt = f"გააანალიზე შემდეგი პროდუქტის მიმოხილვა და დააბრუნე პასუხი სქემის მიხედვით:\n\n{review_text}"
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == "__main__":
    test_reviews = [
        "This laptop is fast, lightweight, and has an excellent display. However, its battery life could be better.",
        "The phone is slow, overheats frequently, and the camera quality is disappointing.",
        "The headphones have average sound quality. They are comfortable, but the price is relatively high."
    ]

    for i, review in enumerate(test_reviews, 1):
        print(f"\n--- ტექსტი {i} ---")
        print(f"მიმოხილვა: {review}")
        print("\nშედეგი AI ასისტენტისგან:")
        try:
            result = evaluate_review(review)
            print(result)
        except Exception as e:
            print(f"შეცდომა: {e}")