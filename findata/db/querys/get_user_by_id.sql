SELECT id, name, lastname, mail, rol, phone, contry, age, ocupation
FROM finpartnerts 
WHERE id = %s;

-- usado en la funcion mantener_seccion 