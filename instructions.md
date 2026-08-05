# API Calling with JSON

> **How you'll submit this lab**
>
> This repo is your lab. Fork it, do the work described below in your fork, then open a pull
> request back into this repository. An AI reviewer will check your PR against `rubric.md` and
> leave feedback directly on the PR. See `README.md` for the full workflow.

**Scenario**  
You're continuing your work on the automated product listing generator. Now, your clients want to provide product information via JSON API requests instead of just using images. You need to build a robust system that validates incoming JSON data using Pydantic, ensures data quality, and processes client requests reliably. This lab builds on your previous ChatGPT API work and adds data validation capabilities.

**Learning Objectives**
- [ ] Understand JSON schema validation
- [ ] Use Pydantic for data validation
- [ ] Create Pydantic models for structured data
- [ ] Validate API request payloads
- [ ] Handle validation errors gracefully
- [ ] Integrate validation with API processing
- [ ] Build a complete API workflow with validation

**Estimated Time:** 120-150 minutes

**Prerequisites:**
- [ ] Completion of Lab M1.05 (API Calling to ChatGPT)
- [ ] Understanding of JSON data format
- [ ] Basic knowledge of Python classes
- [ ] Familiarity with error handling

---

## Introduction

Welcome to the API Calling with JSON lab! This lab extends your product listing generator by adding robust data validation using Pydantic. You'll learn how to ensure data quality before processing, which is crucial for production systems.

**What you'll build:**
- Pydantic models for product data validation
- JSON validation system
- Integration with your existing ChatGPT API workflow
- Error handling for invalid data
- A complete validated API pipeline

**Why this matters:**
In real-world applications, you can't trust that incoming data is correct. Validation prevents errors, improves security, and ensures data quality. Pydantic is the industry standard for data validation in Python, used by major frameworks like FastAPI.

**Success criteria:**
- [ ] Create Pydantic models for product data
- [ ] Validate JSON input successfully
- [ ] Handle validation errors appropriately
- [ ] Integrate validation with API processing
- [ ] Process validated requests end-to-end

---

## Background Story

Your product listing generator is working well, but now clients want to send product information via API requests. However, you've noticed that:

- Some clients send incomplete data
- Data types are sometimes wrong (price as string instead of number)
- Required fields are missing
- Invalid values are provided (negative prices, empty names)

You need to validate all incoming data before processing to ensure:
- Data quality and consistency
- System reliability
- Better error messages for clients
- Prevention of API errors downstream

Pydantic will help you create validation rules and automatically check all incoming data.

---

## Step-by-Step Instructions

### Step 1: Setting Up Pydantic

**Objective:** Install Pydantic and understand its basic usage. We mentioned Pydantic in previous labs, but now it's time to dive deeper into its capabilities for yourself.

**What to do:**
1. Install Pydantic
2. Create a simple validation example
3. Understand how Pydantic works

**Required packages:**
```bash
pip install pydantic
```

As usual, here is a code template to get you started:

**Code template:**
```python
"""
API with JSON Validation using Pydantic - Complete Solution
Validate JSON input using Pydantic before processing
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
import json

print("="*50)
print("PYDANTIC BASICS")
print("="*50)

class SimpleProduct(BaseModel):
    """A simple product model for validation."""
    name: str
    price: float
    quantity: int = 1  # Default value
    
    @validator('price')
    def price_must_be_positive(cls, v):
        """Validate that price is positive."""
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        """Validate that quantity is positive."""
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

# Test validation
print("\n1. Valid data:")
try:
    product1 = SimpleProduct(name="Widget", price=10.99, quantity=5)
    print(f"  ✓ Valid: {product1.name} - ${product1.price}")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n2. Invalid data (negative price):")
try:
    product2 = SimpleProduct(name="Widget", price=-10.99)
except Exception as e:
    print(f"  ✗ Validation error (expected): {e}")

print("\n✓ Pydantic basics working!")

```

Tip: if you are not using the Field helper from Pydantic, this code will need to be adapted.

Tip: if you are not using Optional types in your model fields, this code will need to be adapted.

Tip: if you are not serializing JSON in this step, this code will need to be adapted.

**Expected outcome:** You should see how Pydantic validates data and raises errors for invalid input.

**Checkpoint:** Verify that Pydantic is installed and basic validation works.

---

### Step 2: Creating Product Data Models

**Objective:** Design Pydantic models for product listing requests.

**What to do:**
1. Define the structure of product data for YOUR previous listing generator
2. Create Pydantic models with validation rules that make sense of your use case.
3. Add custom validators for business logic

Tip: if you have a hard time getting started, refer to the product fields used in your previous lab. 

Tip: Consider fields like name, price, category, description, additional_info, etc. If you get overwhelmed, start simple and add complexity gradually.

Tip: If you are really stuck, ask ChatGPT to help you understand the business logic behind product data validation.

**Expected outcome:** You should have working Pydantic models that validate product data correctly.

**Checkpoint:** Verify that:
- Valid data passes validation
- Invalid data raises appropriate errors
- Required fields are enforced
- Custom validators work correctly

---

### Step 3: Validating JSON Input

**Objective:** Validate JSON data from files.

**What to do:**
1. Generate example JSON files (valid and invalid) using the structure defined in Step 2. You can generate these using examples from your previous lab or ask ChatGPT to help you create them.
2. Write a function to load JSON data and validate it using your Pydantic models.
3. Define a logic to handle validation errors 
4. Return validated data

**Expected outcome:** You should be able to validate JSON data and get clear error messages for invalid input.

**Checkpoint:** Verify that validation works for valid and invalid JSON.

---

### Step 4: Integrating with ChatGPT API

**Objective:** Combine validation with your existing ChatGPT API workflow.

**What to do:**
1. Import your previous ChatGPT API code
2. Validate input before processing
3. Process only validated requests
4. Return appropriate responses
5. Validate that the output is also in a standardized format (for example, by using Pydantic models)


**Expected outcome:** You should have a complete workflow that validates the input BEFORE processing and the output AFTER processing.

**Checkpoint:** Verify that:
- Invalid data is rejected before API calls
- Valid data is processed successfully
- Errors are handled gracefully

---

### Step 5: Handling Multiple Requests

**Objective:** Process a list of incoming JSON requests in one run.

**What to do:**
1. Load a list of request payloads from a JSON file
2. Validate each payload with your Pydantic model
3. Process valid requests and collect structured errors for invalid ones
4. Return a summary of successes and failures

**Expected outcome:** You can process batches while preserving clear per-request validation feedback.

**Checkpoint:** Verify that your batch run handles mixed valid/invalid requests without stopping the full pipeline.

---

### Step 6: Creating a Client Request Handler

**Objective:** Wrap validation + processing into a reusable handler function.

**What to do:**
1. Create a `handle_client_request(payload: dict)` function
2. Validate input, call your processing logic, and validate output
3. Return a consistent response shape for success and error cases

**Expected outcome:** You have one reusable entry point for future API endpoints or scripts.

**Checkpoint:** Verify the handler returns predictable JSON for both valid and invalid payloads.

---
## Bonus Challenge: New Dataset from Scratch

**Objective:** Apply your validation skills to a completely new dataset.

**Task:** Choose a new dataset (from Kaggle, HuggingFace, or create your own) and:

1. **Analyze the dataset structure**
   - What fields does it have?
   - What are the data types?
   - What validation rules make sense?

2. **Create Pydantic models**
   - Design models that match the dataset
   - Add appropriate validation rules
   - Include custom validators for business logic

3. **Build a validation pipeline**
   - Load data from the dataset
   - Validate each record
   - Report validation results
   - Handle invalid records appropriately

4. **Process validated data**
   - Use the validated data for some purpose (analysis, API calls, etc.)
   - Demonstrate the value of validation

5. **Connect with ChatGPT**
    - Integrate with ChatGPT API to process validated data
    - Show how validation improves the workflow

6. **Validate ChatGPT output**
    - Ensure the responses from ChatGPT also conform to expected formats using Pydantic models

**Suggested Datasets:**
- **Customer Reviews Dataset:** Validate review data (rating, text, date, etc.)
- **Real Estate Listings:** Validate property data (price, location, features)
- **Employee Records:** Validate HR data (salary, department, dates)
- **E-commerce Orders:** Validate order data (items, prices, customer info)

**Deliverables:**
- Pydantic models for your chosen dataset
- Validation code
- Results showing validation statistics
- Brief report on your findings

---

## Submission Guidelines

### What to Submit

**Required deliverables:**
- [ ] Your complete `api_json_validation.py` file with:
  - Pydantic models
  - Validation functions
  - Integration with ChatGPT API
  - Client request handler
- [ ] Example JSON files (valid and invalid examples)
- [ ] Screenshots or output showing:
  - Successful validation
  - Validation errors
  - Complete workflow execution
- [ ] A brief report (1 page) including:
  - How Pydantic validation works
  - Benefits of validation
  - Challenges you faced
  - Improvements you made

**Bonus (if completed):**
- [ ] Pydantic models for new dataset
- [ ] Validation results and statistics
- [ ] Brief analysis report

### How to Submit

**Upload your work:**
1. **For code files:** Upload your Python scripts
2. **For JSON files:** Upload example request files
3. **For screenshots:** Upload PNG or JPG images
4. **For reports:** Upload PDF or text files

**Important notes:**
- Include comments explaining your validation logic
- Show examples of both valid and invalid data
- Document your Pydantic models
- Explain your validation rules

**Due date:** Check with your instructor for the specific due date.

---

## Troubleshooting

**Common issues and solutions:**

**Issue 1: "Pydantic validation errors are unclear"**
- **Solution:** 
  - Use `try/except` to catch ValidationError
  - Access `error.errors()` for detailed error information
  - Print error details for debugging

**Issue 2: "Optional fields are required"**
- **Solution:** 
  - Use `Optional[type] = None` for optional fields
  - Or use `Field(default=None)` for more control
  - Check your model definition

**Issue 3: "Custom validator not working"**
- **Solution:** 
  - Make sure validator decorator is correct: `@validator('field_name')`
  - Check validator function signature
  - Use `pre=True` if you need to validate before type conversion

**Issue 4: "JSON parsing fails before validation"**
- **Solution:** 
  - Validate JSON format first with `json.loads()`
  - Handle JSONDecodeError separately
  - Provide clear error messages

**Issue 5: "Validation is too strict/too lenient"**
- **Solution:** 
  - Adjust Field constraints (min_length, max_length, gt, lt)
  - Modify custom validators
  - Use `Config.extra = 'ignore'` to ignore extra fields
  - Use `Config.extra = 'allow'` to allow extra fields

**Issue 6: "Integrating with existing code is difficult"**
- **Solution:** 
  - Convert Pydantic models to dicts with `.dict()`
  - Use `.json()` for JSON serialization
  - Access fields as attributes (e.g., `product.name`)

---

## Additional Resources

**Reference materials:**
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pydantic Validators Guide](https://docs.pydantic.dev/usage/validators/)
- [JSON Schema Validation](https://json-schema.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

**Tools and software:**
- [Pydantic Playground](https://pydantic-docs.helpmanual.io/) - Test Pydantic models
- [JSON Schema Validator](https://www.jsonschemavalidator.net/) - Validate JSON schemas
- [FastAPI](https://fastapi.tiangolo.com/) - Framework using Pydantic

**Further reading:**
- [Data Validation Best Practices](https://docs.pydantic.dev/usage/validators/)
- [API Design with Validation](https://fastapi.tiangolo.com/tutorial/body/)
- [Type Safety in Python](https://realpython.com/python-type-checking/)

---

## To-Do List

- [ ] Complete Step 1: Setting Up Pydantic
- [ ] Complete Step 2: Creating Product Data Models
- [ ] Complete Step 3: Validating JSON Input
- [ ] Complete Step 4: Integrating with ChatGPT API
- [ ] Complete Step 5: Handling Multiple Requests
- [ ] Complete Step 6: Creating a Client Request Handler
- [ ] Test with various valid and invalid inputs
- [ ] Document your validation rules
- [ ] (Optional) Complete Bonus Challenge
- [ ] Submit your work

---

## Learning Reflection

After completing this lab, reflect on what you've learned:

1. **Data Validation:** Why is validation important before processing data?
2. **Pydantic:** What advantages does Pydantic provide over manual validation?
3. **Error Handling:** How does validation improve error messages and debugging?
4. **Type Safety:** How do type hints and Pydantic work together?
5. **API Design:** How does validation improve API reliability?
6. **Best Practices:** What validation patterns are most useful?

**Key takeaways:**
- Validation prevents errors and improves data quality
- Pydantic provides automatic validation with clear error messages
- Type hints make code more maintainable and less error-prone
- Validating early (before processing) saves time and resources
- Good validation improves user experience with clear error messages
- Validation is essential for production systems

These skills are crucial for building reliable, production-ready applications that handle real-world data correctly.

---

*Excellent work on building a robust validation system! You've learned essential skills for ensuring data quality in production applications.*
