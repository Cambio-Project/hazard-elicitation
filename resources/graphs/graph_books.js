let graph = {
  "nodes": [
    {
      "label": "users",
      "id": 0
    },
    {
      "label": "frontend",
      "id": 1
    },
    {
      "label": "books",
      "id": 2
    }
  ],
  "links": [
    {
      "label": "authentication",
      "source": 0,
      "target": 0
    },
    {
      "label": "users.GET",
      "source": 0,
      "target": 0
    },
    {
      "label": "users.POST",
      "source": 0,
      "target": 0
    },
    {
      "label": "getUsers",
      "source": 1,
      "target": 0
    },
    {
      "label": "getCatalog",
      "source": 1,
      "target": 2
    },
    {
      "label": "createBook",
      "source": 1,
      "target": 0
    },
    {
      "label": "createBook",
      "source": 1,
      "target": 2
    },
    {
      "label": "createUser",
      "source": 1,
      "target": 0
    },
    {
      "label": "books.GET",
      "source": 2,
      "target": 2
    },
    {
      "label": "books.POST",
      "source": 2,
      "target": 2
    }
  ]
};