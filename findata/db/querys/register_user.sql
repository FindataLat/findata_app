INSERT INTO finpartnerts (
    name, lastname, phone, contry, age, mail, pass, rol, ocupation, 
    created_at, updated_at
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
) RETURNING name;