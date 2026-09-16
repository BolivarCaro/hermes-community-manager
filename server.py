import json
import logging
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
	level=logging.INFO,
	stream=sys.stderr,
	format="%(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP("community-manager")

CATALOG_PATH = Path(__file__).resolve().parent / "data" / "catalog.json"

@mcp.tool()
def get_product_info(product_name: str) -> dict:
	"""Consulta precio, descripción y stock por nombre exacto del producto. 
	No distingue mayúsculas de minúsculas.
	Úsala cuando necesites datos del catálogo para responder un comentario.
	Si el producto no existe en el catálogo, devuelve found-False.
	"""
	
	name = product_name.strip()
	if not name:
		return {"error": "Debes indicar el nombre del producto."}
	logger.info("Consulta al catálogo: %r", name)
	try:
		catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
	except (OSError, json.JSONDecodeError):
		logger.exception("No se pudo leer el catálogo")
		return {"error": "El catálogo no está disponible en este momento."}
	
	for product in catalog["products"]:
		if product["name"].casefold() == name.casefold():
			return {
				"found": True,
				"product": product,
				"source": "data/catalog.json",
			}
	return {
			"found": False,
			"query": name,
			"message": "Producto no encontrado en el catálogo.",
		}
if __name__ == "__main__":
	mcp.run(transport="stdio")
