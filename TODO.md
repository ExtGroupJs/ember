# TODO

Las producciones pueden ser de cualquier subclasificación del plan.

Adicionar sistema de logs para visualizar acciones en el sistema, solo visualizar por admins. No editable.




Nombres en listado mostrarlos completo, sin chunk. Alternativamente mostrar el nombre completo como tooltip.

En los planes poner la suma anates de guardar.
En  la unidad de medidas no poner la sigla, sino el nombre de la unidad completo.
Deshabilitar formularios hasta recibir respuesta en operaciones de crear o editar.
Revisar ordenar por UEB en planes
revisar precios minoristas y mayoristas en producción, ahora mismo admiten números negativos
En la producción, como ahora los planes son de productos específicos, en la producción solo escoger el plan (revisar en el modelo la asociación de la producción, que debe ser solo al plan, no debe haber referencia directa al producto)

Revisar con calma: En los planes, solo poner clasificaciones hijas, es decir, de productos finales, NO clasificaciones con hijos.

Quitar restricción de unique al nombre del plan. Para todos los meses el valor por default es 0.
poner un flag `extra_plan` que se setea en true si el total es 0

## Sobre informes
Hacerlos por los PDF de ejemplo, con filtros de todo...