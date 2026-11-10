import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from product_models import ProductRequest


load_dotenv()


def load_json_payload(file_path: str) -> dict:
    """Load JSON data from a file."""

    path = Path(file_path)
    return json.loads(path.read_text(encoding="utf-8"))


def create_product_prompt(product: ProductRequest) -> str:
    """Create a prompt from validated product data."""

    return f"""
Create a professional e-commerce product listing.

Product name: {product.name}
Price: ${product.price:.2f}
Category: {product.category}
Description: {product.description or "Not provided"}
Additional information: {product.additional_info or "Not provided"}
Image path: {product.image_path or "Not provided"}

Return:
1. A compelling product title
2. A detailed product description
3. Five key features
4. SEO keywords
""".strip()


def process_product_request(payload: dict) -> dict:
    """
    Validate a product request before calling the ChatGPT API.
    """

    # Validation happens before any API call.
    try:
        product = ProductRequest.model_validate(payload)

    except ValidationError as error:
        return {
            "success": False,
            "stage": "input_validation",
            "error_type": "validation_error",
            "errors": [
                {
                    "field": detail["loc"],
                    "message": detail["msg"],
                }
                for detail in error.errors()
            ],
        }

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not model:
        return {
            "success": False,
            "stage": "configuration",
            "error_type": "missing_configuration",
            "errors": [
                "OPENAI_API_KEY and OPENAI_MODEL must be set in .env"
            ],
        }

    client = OpenAI(api_key=api_key)
    prompt = create_product_prompt(product)

    try:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are an expert e-commerce copywriter. "
                "Create accurate and persuasive product listings."
            ),
            input=prompt,
        )

    except Exception as error:
        return {
            "success": False,
            "stage": "api_call",
            "error_type": "api_error",
            "errors": [str(error)],
        }

    return {
        "success": True,
        "stage": "completed",
        "validated_product": product.model_dump(),
        "listing": response.output_text,
    }


if __name__ == "__main__":
    try:
        payload = load_json_payload("valid_product.json")
        result = process_product_request(payload)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError as error:
        print(
            json.dumps(
                {
                    "success": False,
                    "stage": "json_parsing",
                    "error_type": "invalid_json",
                    "errors": [str(error)],
                },
                indent=2,
            )
        )