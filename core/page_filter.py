from rest_framework.response import Response
import math


def pages_filter(self, request, Model, *args, **kwargs):
        page = request.query_params.get('page', 1)
        size = request.query_params.get('size', 10)
        sort = request.query_params.get('sort', 'id')
        direction = request.query_params.get('direction', 'asc')

        page = int(page)
        size = int(size)

        if page < 1:
            page=1
        if size < 1:
            size=1

        start_index = (page-1) * size
        end_index = (start_index + size)


        if direction.lower() == 'asc':
            try:
                Messages = Model.objects.order_by(sort)[start_index:end_index]
            except:
                Messages = Model.objects.order_by(sort)[start_index]
            
        else:
            try:
                Messages = Model.objects.order_by(f"-{sort}")[start_index:end_index]
            except:
                Messages = Model.objects.order_by(f"-{sort}")[start_index]


        serializer = self.serializer_class(Messages, many=True, context={"request": request}, *args, **kwargs)
        total_Messages = Model.objects.count()
        total_pages = math.ceil(total_Messages/size)
        num_elements = len(Messages)
        data = {
            "totalPages": total_pages,
            "totalElements": total_Messages,
            "first": start_index+1,
            "last": num_elements,
            "number": num_elements,
            "sort": {
                "sorted": True,
                "unsorted": False,
                "empty": False
            },
            "numberOfElements": num_elements,
            "pagable": {
                "sort": {
                    "sorted": True,
                    "unsorted": False,
                    "empty": False
                },
                "pageNumber": page,
                "pageSize": size,
                "paged": True,
                "unpaged": False,
                "offset": start_index
            },
            "size": size,
            "content": serializer.data,
            "empty": len(serializer.data) == 0
        }
        return Response(data)