import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="prior_db"
    )


def save_form_data(
    emp_id,
    name_designation,
    scale_pay,
    purpose,
    property_type,
    probable_date,
    mode,
    location_7a,
    description_7b,
    hold_type_7c,
    interest_7d,
    ownership_7e,
    price,
    finance_source_main,
    personal_savings_9a,
    other_sources_9b,
    sanction_details,
    party_name_11a,
    party_relation_11b,
    official_dealings_11c,
    transaction_mode_11d,
    additional_facts,
    station,
    submission_date
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO prior_intimation_full (
            emp_id,
            name_designation,
            scale_pay,
            purpose,
            property_type,
            probable_date,
            mode,
            location_7a,
            description_7b,
            hold_type_7c,
            interest_7d,
            ownership_7e,
            price,
            finance_source_main,
            personal_savings_9a,
            other_sources_9b,
            sanction_details,
            party_name_11a,
            party_relation_11b,
            official_dealings_11c,
            transaction_mode_11d,
            additional_facts,
            station,
            submission_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        emp_id,
        name_designation,
        scale_pay,
        purpose,
        property_type,
        probable_date,
        mode,
        location_7a,
        description_7b,
        hold_type_7c,
        interest_7d,
        ownership_7e,
        price,
        finance_source_main,
        personal_savings_9a,
        other_sources_9b,
        sanction_details,
        party_name_11a,
        party_relation_11b,
        official_dealings_11c,
        transaction_mode_11d,
        additional_facts,
        station,
        submission_date
    ))

    connection.commit()
    cursor.close()
    connection.close()