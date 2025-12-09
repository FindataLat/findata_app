UPDATE finpartnerts
SET
    name = %s,
    lastname = %s,
    phone = %s,
    contry = %s,
    age = %s,
    mail = %s,
    pass = %s,
    rol = %s,
    ocupation = %s,
    updated_at = CURRENT_TIMESTAMP
WHERE id = %s
RETURNING name;
