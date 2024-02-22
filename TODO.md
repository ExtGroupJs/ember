En el editar de unidades de medida, permitir que sirvan para el plan
En el plan c'omo se pone la fecha
Para la fecha si pudieras encontrar un selector sería genial
{
    "production_date": [
        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
    ]
}





# FE
- No dejar scroll en el menú
- en la produccion, el listado de embase agrupador y en el listado (formato), no usar el nombre, sino la conformacion de cantidadXml-?????
- En el adicionar y editar embases (empaques individuales) adicionar el campo Material (Vidrio o PEP)
- Cuando se van a crear empaques agrupadores desde el menú, comenzar desde 2, si es uno solo, se debe marcar desde el empaque individual.
- Quitar los fields de "destination", "entity" del formulario de creación/edición de la producción.
- Adicionar en el formulario de creación/edición de la producción la selección (obligatoria) del plan al que responde la producción
- Adicionar un selector de productos en el formulario de creación/edición de la producción, dicho producto se debe halar de /product-gestion/plan/{id}/allowed-products/ donde el id es el del plan seleccionado previamente.
- Hacer formulario para creación del plan, es muy similar al de producción actual, pero además lleva año y mes, además en vez de "producto" se debe seleccionar una "clasificación", este código se puede robar de donde se hace algo similar en "productos"
- En el formulario de creación/edición de las unidades de medida, adicionar un campo "usar en planificación" que se corresponde con el field "used_for_planning"
- Cuando se elabora o modifica un plan, y se quiera setear la unidad de medida del plan, se debe halar de /product-gestion/measurement-unit/ como hasta ahora, pero con el filtro del used_for_planning seteado a true, sería así: /product-gestion/measurement-unit/?used_for_planning=true



# BE
1. Revisar subida de fotos (png).

despues que este todo terminado, el tiene que generar
el mensual (es la suma de todos los anteriores)
el acumulado hasta el mes deseado.
