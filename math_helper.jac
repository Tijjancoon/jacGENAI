 import os;
import from byllm.llm { Model }

# Geting API key from environment
glob gemini_api_key = os.getenv("GEMINI_API_KEY");

# uses gemini api key from env
glob llm = Model(
    model_name="gemini/gemini-2.0-flash",
    verbose=False,
    api_key=gemini_api_key
);

def explain_addition(number1: int, number2: int) -> str by llm(
    doc="Explain this addition problem step by step like a patient math teacher."
);

walker MathHelper {
    has number1: int;
    has number2: int;

    can add with entry {
        result = self.number1 + self.number2;
        print(self.number1, "+", self.number2, "=", result);
        print("AI Explains:");
        print(explain_addition(number1=self.number1, number2=self.number2));
    }
}

with entry:__main__ {
    root spawn MathHelper(number1=5, number2=3);
}