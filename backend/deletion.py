from vector_store import collection

all_items = collection.get()

if all_items["ids"]:
    collection.delete(
        ids=all_items["ids"]
    )

print("Collection cleared")