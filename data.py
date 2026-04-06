FINANCIAL_DOCS = [
    """Q4 2024 Accounts Receivable Report.
    Constructora Norteña S.A. - Invoice INV-2024-0892 - $145,000 USD.
    Due date: October 31 2024. Status: OVERDUE 45 days.
    Contact: Carlos Mendoza - cmendoza@cnortena.com""",

    """Retail Express LLC - Invoice INV-2024-0901 - $67,500 USD.
    Due date: November 14 2024. Status: PAID on November 10 2024.""",

    """Logistica del Pacifico - Invoice INV-2024-0923 - $230,000 USD.
    Due date: December 1 2024. Status: PENDING - 12 days until due.""",

    """Q4 2024 Budget vs Actual Report.
    Operations Department: Budget $500,000. Actual $487,200. 
    Variance: -$12,800 (2.6% under budget).
    Marketing Department: Budget $120,000. Actual $134,500.
    Variance: +$14,500 (12.1% OVER budget). CFO approval required.""",

    """November 2024 Cash Flow Statement.
    Opening balance: $1,240,000 USD.
    Projected inflows: $890,000 USD.
    Projected outflows: $760,000 USD.
    Projected closing balance: $1,370,000 USD.
    Days of liquidity: 47 days."""
]

EVAL_DATASET = [
    {
        "question": "Which invoices are overdue?",
        "ground_truth": "Invoice INV-2024-0892 from Constructora Norteña S.A. for $145,000 USD is overdue by 45 days."
    },
    {
        "question": "Which department is over budget?",
        "ground_truth": "Marketing department is over budget by $14,500 USD, which is 12.1% above their $120,000 budget. CFO approval is required."
    },
    {
        "question": "What is the projected cash flow closing balance?",
        "ground_truth": "The projected closing balance for November 2024 is $1,370,000 USD with 47 days of liquidity."
    },
    {
        "question": "What is the status of the Logistica del Pacifico invoice?",
        "ground_truth": "Invoice INV-2024-0923 from Logistica del Pacifico for $230,000 USD is pending with 12 days until the due date of December 1 2024."
    },
    {
        "question": "How much is Operations department under budget?",
        "ground_truth": "Operations department is $12,800 under budget, which is 2.6% below their $500,000 budget."
    }
]