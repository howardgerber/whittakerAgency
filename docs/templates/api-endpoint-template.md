# API Endpoint: [Endpoint Name]

**Endpoint:** `[HTTP METHOD] /api/[path]`  
**Authentication:** [Required/Optional/None]  
**Added:** [Date]  
**Last Modified:** [Date]

## Description
Brief description of what this endpoint does.

## Request

### URL Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | [Description] |
| `status` | string | No | [Description] |

### Query Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number for pagination |
| `pageSize` | integer | No | 20 | Number of items per page |

### Request Body
```json
{
  "propertyName": "string",
  "anotherProperty": 123,
  "nestedObject": {
    "nested": "value"
  }
}
```

### Headers
```
Authorization: Bearer [token]  (if authentication required)
Content-Type: application/json
```

## Response

### Success Response (200 OK)
```json
{
  "id": 123,
  "propertyName": "string",
  "createdAt": "2025-08-28T10:30:00Z",
  "data": [
    {
      "item": "value"
    }
  ]
}
```

### Error Responses

#### 400 Bad Request
```json
{
  "message": "Validation error description",
  "errors": {
    "fieldName": ["Field is required"]
  }
}
```

#### 401 Unauthorized
```json
{
  "message": "Authentication required"
}
```

#### 404 Not Found
```json
{
  "message": "Resource not found"
}
```

## Examples

### cURL Example
```bash
curl -X GET "https://api.example.com/api/endpoint/123?page=1" \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json"
```

### JavaScript Example
```javascript
const response = await apiService.getEndpoint(123, {
  page: 1,
  pageSize: 20
});
```

### C# Controller Example
```csharp
[HttpGet("{id}")]
public async Task<ActionResult<ResponseType>> GetEndpoint(int id)
{
    // Implementation
}
```

## Business Logic
Explanation of any complex business rules or calculations performed.

## Database Queries
Description of main database operations performed.

## Performance Notes
- Expected response time
- Caching behavior
- Rate limiting considerations

## Related Endpoints
- `GET /api/related-endpoint` - [Description]
- `POST /api/related-endpoint` - [Description]

## Changelog
| Date | Change | Author |
|------|--------|---------|
| 2025-08-28 | Initial creation | [Author] |