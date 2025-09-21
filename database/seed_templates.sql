-- Insert legal document templates and knowledge base
-- This script populates the legal_templates table with common document types

-- Rental Agreement Template
INSERT INTO legal_templates (
    name, category, subcategory, description, 
    common_clauses, risk_factors, key_terms_to_check, red_flags, 
    standard_protections, simplified_language, question_templates, 
    jurisdiction, applicable_laws
) VALUES (
    'Standard Rental Agreement',
    'rental_agreement',
    'residential_lease',
    'Template for analyzing residential rental agreements and lease contracts',
    '[
        "rent_amount_clause",
        "lease_duration",
        "security_deposit",
        "maintenance_responsibilities",
        "pet_policy",
        "subletting_restrictions",
        "termination_conditions",
        "late_fee_policy",
        "utility_responsibilities",
        "property_access_rights"
    ]'::jsonb,
    '[
        {
            "risk": "excessive_security_deposit",
            "description": "Security deposit exceeding legal limits",
            "severity": "high"
        },
        {
            "risk": "automatic_renewal",
            "description": "Automatic lease renewal without proper notice",
            "severity": "medium"
        },
        {
            "risk": "maintenance_burden",
            "description": "Tenant responsible for major repairs",
            "severity": "high"
        },
        {
            "risk": "unreasonable_restrictions",
            "description": "Overly restrictive rules about guests or use",
            "severity": "medium"
        }
    ]'::jsonb,
    '[
        "monthly_rent",
        "security_deposit",
        "lease_term",
        "notice_period",
        "late_fees",
        "pet_deposit",
        "maintenance_clause",
        "termination_clause"
    ]'::jsonb,
    '[
        "Security deposit over 2 months rent",
        "No return procedure for deposits",
        "Tenant pays for normal wear and tear",
        "Landlord can enter without notice",
        "No grace period for late rent",
        "Automatic lease renewal clause",
        "Tenant responsible for major repairs"
    ]'::jsonb,
    '[
        "Reasonable notice for entry (24-48 hours)",
        "Clear deposit return procedures",
        "Grace period for late payments",
        "Habitability guarantees",
        "Right to quiet enjoyment"
    ]'::jsonb,
    '{
        "rent_amount": "This is how much you pay each month for rent",
        "security_deposit": "Money held by landlord for damages - should be returned if you leave the place clean",
        "lease_term": "How long your rental agreement lasts",
        "maintenance": "Who is responsible for fixing things when they break"
    }'::jsonb,
    '[
        "How much is my monthly rent?",
        "When is rent due each month?",
        "How much is the security deposit?",
        "What happens if I pay rent late?",
        "Can I have pets?",
        "Can the landlord enter my apartment anytime?",
        "Who pays for repairs?",
        "How do I get my deposit back?",
        "Can I break the lease early?",
        "What utilities do I pay for?"
    ]'::jsonb,
    'US',
    '[
        "Fair Housing Act",
        "State landlord-tenant laws",
        "Local rent control ordinances",
        "Security deposit regulations"
    ]'::jsonb
);

-- Loan Contract Template
INSERT INTO legal_templates (
    name, category, subcategory, description,
    common_clauses, risk_factors, key_terms_to_check, red_flags,
    standard_protections, simplified_language, question_templates,
    jurisdiction, applicable_laws
) VALUES (
    'Personal Loan Agreement',
    'loan_contract',
    'personal_loan',
    'Template for analyzing personal loan agreements and credit contracts',
    '[
        "principal_amount",
        "interest_rate",
        "repayment_schedule",
        "default_conditions",
        "late_payment_penalties",
        "prepayment_options",
        "collateral_requirements",
        "personal_guarantees",
        "acceleration_clause",
        "governing_law"
    ]'::jsonb,
    '[
        {
            "risk": "variable_interest_rate",
            "description": "Interest rate can increase over time",
            "severity": "high"
        },
        {
            "risk": "balloon_payment",
            "description": "Large final payment required",
            "severity": "high"
        },
        {
            "risk": "cross_default",
            "description": "Default on other loans triggers this loan default",
            "severity": "medium"
        },
        {
            "risk": "personal_guarantee",
            "description": "Personal assets at risk beyond collateral",
            "severity": "high"
        }
    ]'::jsonb,
    '[
        "principal_amount",
        "interest_rate",
        "apr",
        "payment_amount",
        "payment_frequency",
        "loan_term",
        "default_rate",
        "late_fees",
        "prepayment_penalty",
        "collateral"
    ]'::jsonb,
    '[
        "Variable or adjustable interest rates",
        "Prepayment penalties over 2%",
        "Personal guarantees required",
        "Cross-default clauses",
        "Balloon payments",
        "Excessive late fees",
        "Short cure periods for default"
    ]'::jsonb,
    '[
        "Fixed interest rate",
        "Reasonable grace period for payments",
        "Clear default and cure procedures",
        "Right to prepay without penalty",
        "Detailed payment schedule"
    ]'::jsonb,
    '{
        "principal": "The amount of money you are borrowing",
        "interest_rate": "The percentage charged for borrowing the money",
        "apr": "Annual Percentage Rate - the true yearly cost of the loan",
        "collateral": "Property that secures the loan - can be taken if you do not pay",
        "default": "What happens if you miss payments or break the agreement"
    }'::jsonb,
    '[
        "How much am I borrowing?",
        "What is my interest rate?",
        "What are my monthly payments?",
        "When are payments due?",
        "What happens if I miss a payment?",
        "Can I pay off the loan early?",
        "What collateral is required?",
        "What constitutes default?",
        "Can the interest rate change?",
        "What are the late fees?"
    ]'::jsonb,
    'US',
    '[
        "Truth in Lending Act",
        "Fair Credit Reporting Act",
        "State usury laws",
        "Consumer protection regulations"
    ]'::jsonb
);

-- Employment Contract Template
INSERT INTO legal_templates (
    name, category, subcategory, description,
    common_clauses, risk_factors, key_terms_to_check, red_flags,
    standard_protections, simplified_language, question_templates,
    jurisdiction, applicable_laws
) VALUES (
    'Employment Agreement',
    'employment_contract',
    'full_time_employment',
    'Template for analyzing employment contracts and job agreements',
    '[
        "job_title_duties",
        "compensation_structure",
        "benefits_package",
        "working_hours",
        "termination_conditions",
        "non_compete_clause",
        "confidentiality_agreement",
        "intellectual_property",
        "probationary_period",
        "dispute_resolution"
    ]'::jsonb,
    '[
        {
            "risk": "broad_non_compete",
            "description": "Overly restrictive non-compete agreement",
            "severity": "high"
        },
        {
            "risk": "at_will_employment",
            "description": "Can be terminated without cause",
            "severity": "medium"
        },
        {
            "risk": "unpaid_overtime",
            "description": "No overtime compensation despite long hours",
            "severity": "medium"
        },
        {
            "risk": "broad_ip_assignment",
            "description": "Company claims rights to all your inventions",
            "severity": "high"
        }
    ]'::jsonb,
    '[
        "base_salary",
        "bonus_structure",
        "benefits",
        "vacation_days",
        "sick_leave",
        "termination_notice",
        "non_compete_duration",
        "non_compete_geography",
        "severance_pay",
        "stock_options"
    ]'::jsonb,
    '[
        "Non-compete lasting over 1 year",
        "Non-compete covering entire industry",
        "No severance pay provisions",
        "Broad intellectual property assignments",
        "Mandatory unpaid overtime",
        "No clear termination procedures",
        "Excessive confidentiality terms"
    ]'::jsonb,
    '[
        "Clear job description and duties",
        "Defined compensation and benefits",
        "Reasonable non-compete terms",
        "Fair termination procedures",
        "Overtime compensation"
    ]'::jsonb,
    '{
        "base_salary": "Your regular pay before bonuses or overtime",
        "benefits": "Health insurance, retirement plans, and other perks",
        "non_compete": "Agreement not to work for competitors after leaving",
        "at_will": "Employment can be ended by either party at any time",
        "severance": "Money paid when your job is eliminated"
    }'::jsonb,
    '[
        "What is my salary and how is it paid?",
        "What benefits do I receive?",
        "How much vacation time do I get?",
        "Can I be fired without reason?",
        "What are the non-compete restrictions?",
        "Do I get overtime pay?",
        "What happens to my stock options if I leave?",
        "Can I work freelance on the side?",
        "What is the notice period for termination?",
        "Is there severance pay?"
    ]'::jsonb,
    'US',
    '[
        "Fair Labor Standards Act",
        "Equal Employment Opportunity laws",
        "State employment laws",
        "Non-compete regulations by state"
    ]'::jsonb
);

-- Terms of Service Template
INSERT INTO legal_templates (
    name, category, subcategory, description,
    common_clauses, risk_factors, key_terms_to_check, red_flags,
    standard_protections, simplified_language, question_templates,
    jurisdiction, applicable_laws
) VALUES (
    'Website Terms of Service',
    'terms_of_service',
    'website_tos',
    'Template for analyzing website terms of service and user agreements',
    '[
        "user_obligations",
        "service_description",
        "payment_terms",
        "privacy_policy_reference",
        "intellectual_property_rights",
        "user_generated_content",
        "termination_conditions",
        "limitation_of_liability",
        "dispute_resolution",
        "modifications_to_terms"
    ]'::jsonb,
    '[
        {
            "risk": "broad_liability_waiver",
            "description": "Company not liable for any damages",
            "severity": "high"
        },
        {
            "risk": "unilateral_changes",
            "description": "Terms can be changed without notice",
            "severity": "medium"
        },
        {
            "risk": "broad_content_license",
            "description": "Company gets extensive rights to your content",
            "severity": "medium"
        },
        {
            "risk": "mandatory_arbitration",
            "description": "Cannot sue in court, only arbitration",
            "severity": "medium"
        }
    ]'::jsonb,
    '[
        "service_fees",
        "cancellation_policy",
        "data_usage_rights",
        "content_ownership",
        "liability_limits",
        "arbitration_clause",
        "termination_rights",
        "modification_notice"
    ]'::jsonb,
    '[
        "Complete liability waiver",
        "No refund policy",
        "Unlimited content license to company",
        "Terms can change without notice",
        "Mandatory arbitration clauses",
        "Broad termination rights for company",
        "No data portability rights"
    ]'::jsonb,
    '[
        "Reasonable liability limitations",
        "Clear refund and cancellation policies",
        "User data protection guarantees",
        "Notice period for term changes",
        "Right to export your data"
    ]'::jsonb,
    '{
        "terms_of_service": "Rules you must follow to use the website or app",
        "liability": "Who is responsible when something goes wrong",
        "intellectual_property": "Who owns the content and ideas",
        "arbitration": "Resolving disputes outside of court",
        "data_rights": "How your personal information is used"
    }'::jsonb,
    '[
        "What am I agreeing to?",
        "Can the company change these terms?",
        "What happens to my content?",
        "Can I get a refund?",
        "What data does the company collect?",
        "Can I delete my account?",
        "What if there is a dispute?",
        "Is the company liable for problems?",
        "Can I transfer my data?",
        "How long do these terms last?"
    ]'::jsonb,
    'US',
    '[
        "Consumer protection laws",
        "Privacy regulations",
        "Electronic signatures law",
        "State contract law"
    ]'::jsonb
);