# Requirements Document

## Introduction

This specification defines a comprehensive test suite for the MyWay Career Assessment backend system. The system evaluates users across four quotient domains (IQ, EQ, DQ, AQ), calculates Ikigai scores, and provides career recommendations. The test suite ensures reliability, correctness, and confidence in the scoring algorithms, API endpoints, services, and data integrity.

## Glossary

- **IQ**: Intelligence Quotient - measures logical, numerical, verbal, and spatial reasoning
- **EQ**: Emotional Quotient - measures empathy, social skills, self-awareness, and self-regulation
- **DQ**: Digital Quotient - measures information literacy, creativity, safety awareness, and collaboration
- **AQ**: Adversity Quotient - measures control, ownership, reach, and endurance
- **Ikigai**: Japanese concept representing the intersection of passion, mission, profession, and vocation
- **Profile_Vector**: 16-dimensional vector containing all facet scores for a user
- **Career_Rule**: Configuration defining weights and thresholds for career matching
- **Likert_Scale**: 1-5 rating scale used for EQ, DQ, and AQ questions
- **Facet**: Sub-dimension within each quotient domain (e.g., iq_lr for logical reasoning)
- **Scoring_Algorithm**: Component that calculates domain scores from user answers
- **Career_Mapping_Algorithm**: Component that matches profile vectors to career suggestions
- **Assessment_Service**: Service layer managing assessment lifecycle
- **Career_Service**: Service layer managing career suggestions and analysis

## Requirements

### Requirement 1: Scoring Algorithm Correctness

**User Story:** As a system administrator, I want the scoring algorithms to produce mathematically correct results, so that users receive accurate assessments of their abilities.

#### Acceptance Criteria

1. WHEN a user provides Likert scale answers (1-5) for EQ questions THEN the Scoring_Algorithm SHALL normalize scores to 0-100 range using formula: t̂_j = 25*(t_j-1)
2. WHEN a question has reverse_score=true THEN the Scoring_Algorithm SHALL apply reverse transformation: t_j = (6-x_j) before normalization
3. WHEN calculating facet scores THEN the Scoring_Algorithm SHALL compute the average of all normalized question scores within that facet
4. WHEN calculating domain scores (IQ, EQ, DQ, AQ) THEN the Scoring_Algorithm SHALL compute the average of all facet scores within that domain
5. WHEN IQ questions are answered THEN the Scoring_Algorithm SHALL apply weighted difficulty scoring: S_IQ = 100 * (Σ(d_i * r_i)) / Σ(d_i)
6. FOR ALL valid Likert answers (1-5) THEN the Scoring_Algorithm SHALL produce scores in range [0, 100]
7. WHEN no questions are answered for a facet THEN the Scoring_Algorithm SHALL return 0.0 for that facet score

### Requirement 2: Profile Vector Integrity

**User Story:** As a data analyst, I want profile vectors to accurately represent user assessment results, so that career recommendations are based on correct data.

#### Acceptance Criteria

1. THE Profile_Vector SHALL contain exactly 16 dimensions representing all facets across IQ, EQ, DQ, and AQ domains
2. WHEN converting to vector format THEN the Profile_Vector SHALL maintain consistent ordering: [iq_lr, iq_nr, iq_vr, iq_sr, eq_empathy, eq_social, eq_self_awareness, eq_self_regulation, dq_info_literacy, dq_creativity, dq_safety, dq_collaboration, aq_control, aq_ownership, aq_reach, aq_endurance]
3. FOR ALL facet values in Profile_Vector THEN each value SHALL be constrained to range [0, 100]
4. WHEN a facet value is null THEN the Profile_Vector.to_vector() method SHALL return 0.0 for that position

### Requirement 3: Ikigai Calculation Correctness

**User Story:** As a career counselor, I want Ikigai scores to accurately reflect the balance of user abilities, so that users understand their career alignment.

#### Acceptance Criteria

1. WHEN calculating ikigai_love axis THEN the Ikigai_Algorithm SHALL use formula: (eq_empathy + eq_social + dq_creativity) / 3
2. WHEN calculating ikigai_good_at axis THEN the Ikigai_Algorithm SHALL use formula: (iq_lr + iq_nr + iq_vr + iq_sr) / 4
3. WHEN calculating ikigai_world_needs axis THEN the Ikigai_Algorithm SHALL use formula: (dq_info_literacy + dq_safety + aq_control + aq_ownership) / 4
4. WHEN calculating ikigai_paid_for axis THEN the Ikigai_Algorithm SHALL use formula: (aq_reach + aq_endurance + eq_self_awareness + eq_self_regulation) / 4
5. WHEN calculating harmonic mean THEN the Ikigai_Algorithm SHALL use formula: 4 / (1/love + 1/good_at + 1/world_needs + 1/paid_for)
6. WHEN calculating geometric mean THEN the Ikigai_Algorithm SHALL use formula: (love * good_at * world_needs * paid_for)^(1/4)
7. IF any axis score is zero THEN the Ikigai_Algorithm SHALL return 0.0 for harmonic mean
8. IF any axis score is zero or negative THEN the Ikigai_Algorithm SHALL return 0.0 for geometric mean

### Requirement 4: Career Mapping Algorithm Correctness

**User Story:** As a user, I want career suggestions to accurately match my profile, so that I receive relevant career recommendations.

#### Acceptance Criteria

1. WHEN calculating career fit scores THEN the Career_Mapping_Algorithm SHALL apply weighted scoring based on Career_Rule weights
2. WHEN a profile score exceeds the threshold for a facet THEN the Career_Mapping_Algorithm SHALL include that facet's contribution to the fit score
3. WHEN bonus_keys are defined for a career THEN the Career_Mapping_Algorithm SHALL apply bonus points for high scores in those facets
4. WHEN career fit score is below 30% THEN the Career_Mapping_Algorithm SHALL exclude that career from suggestions
5. THE Career_Mapping_Algorithm SHALL return career suggestions sorted by fit_score in descending order
6. THE Career_Mapping_Algorithm SHALL limit results to maximum 8 career suggestions
7. WHEN a Career_Rule has is_active=false THEN the Career_Mapping_Algorithm SHALL exclude that career from calculations

### Requirement 5: Assessment Service Operations

**User Story:** As a user, I want to complete assessments reliably, so that my progress is tracked and results are saved correctly.

#### Acceptance Criteria

1. WHEN creating a new assessment THEN the Assessment_Service SHALL initialize status as 'in_progress' with answered_questions=0
2. WHEN updating assessment progress THEN the Assessment_Service SHALL correctly update the answered_questions count
3. WHEN completing an assessment THEN the Assessment_Service SHALL set status to 'completed' and record completed_at timestamp
4. WHEN abandoning an assessment THEN the Assessment_Service SHALL set status to 'abandoned' and record completed_at timestamp
5. WHEN retrieving user assessments THEN the Assessment_Service SHALL return assessments ordered by started_at descending
6. WHEN an assessment does not exist THEN the Assessment_Service SHALL return None

### Requirement 6: Career Service Operations

**User Story:** As a user, I want to receive career suggestions and analysis based on my assessment results, so that I can make informed career decisions.

#### Acceptance Criteria

1. WHEN generating career suggestions THEN the Career_Service SHALL create CareerSuggestion records with correct rank ordering
2. WHEN career suggestions already exist THEN the Career_Service SHALL return existing suggestions without regenerating
3. WHEN retrieving career analysis THEN the Career_Service SHALL include ikigai_scores, interpretation, quadrant, and recommendations
4. WHEN comparing careers THEN the Career_Service SHALL return requirements for all requested careers
5. WHEN searching careers THEN the Career_Service SHALL filter by career name (case-insensitive) and limit results

### Requirement 7: API Endpoint Security and Validation

**User Story:** As a system administrator, I want API endpoints to be secure and validate inputs, so that the system is protected from unauthorized access and invalid data.

#### Acceptance Criteria

1. WHEN a request lacks authentication THEN the API SHALL return 401 Unauthorized status
2. WHEN a user attempts to access another user's assessment THEN the API SHALL return 403 Forbidden status
3. WHEN an assessment is not found THEN the API SHALL return 404 Not Found status
4. WHEN request data fails validation THEN the API SHALL return 422 Unprocessable Entity status
5. WHEN comparing fewer than 2 careers THEN the API SHALL return 400 Bad Request status
6. WHEN comparing more than 5 careers THEN the API SHALL return 400 Bad Request status

### Requirement 8: Data Consistency and Edge Cases

**User Story:** As a developer, I want the system to handle edge cases gracefully, so that the application remains stable under unusual conditions.

#### Acceptance Criteria

1. WHEN answers list is empty THEN the Scoring_Algorithm SHALL return 0.0 for all scores
2. WHEN questions list is empty THEN the Scoring_Algorithm SHALL return 0.0 for all scores
3. WHEN profile vector contains all zeros THEN the Ikigai_Algorithm SHALL handle gracefully without division errors
4. WHEN profile vector contains all maximum values (100) THEN all calculations SHALL produce valid results
5. WHEN career rules list is empty THEN the Career_Mapping_Algorithm SHALL return empty suggestions list
6. WHEN answer_value is outside valid range (1-5) THEN the Scoring_Algorithm SHALL handle gracefully

### Requirement 9: Answer Validation

**User Story:** As a system administrator, I want answer validation to ensure data quality, so that scoring is based on complete and valid responses.

#### Acceptance Criteria

1. WHEN validating answers THEN the Validation_Service SHALL verify all required questions are answered
2. WHEN answers are missing for required questions THEN the Validation_Service SHALL return false
3. WHEN answers list is empty THEN the Validation_Service SHALL return false
4. WHEN questions list is empty THEN the Validation_Service SHALL return false

### Requirement 10: Scoring Consistency

**User Story:** As a quality assurance engineer, I want scoring to be deterministic, so that the same inputs always produce the same outputs.

#### Acceptance Criteria

1. FOR ALL valid inputs THEN multiple calls to Scoring_Algorithm with identical inputs SHALL produce identical outputs
2. FOR ALL valid profile vectors THEN multiple calls to Ikigai_Algorithm with identical inputs SHALL produce identical outputs
3. FOR ALL valid profile vectors and career rules THEN multiple calls to Career_Mapping_Algorithm with identical inputs SHALL produce identical outputs
