# Service Layer Patterns

## Overview
Service layer contains ALL business logic: validation, business rules, data access, transformations, calculations, audit logging, external service calls.

## Core Principles
- **Single Responsibility**: One service per domain (`IUserService`, `IProductService`, `IOrderService`)
- **ALL business logic in services**: Controllers have ZERO logic
- **Throw typed exceptions**: `ArgumentException` (validation), `InvalidOperationException` (business rules)
- **Return patterns**: `null` (GET not found), `bool` (UPDATE/DELETE not found), entity (CREATE)

## Service Structure

```csharp
public interface IProductService
{
    Task<ProductDto?> GetProductAsync(int id);              // null = not found
    Task<ProductDto> CreateProductAsync(CreateProductDto);  // throw on error
    Task<bool> UpdateProductAsync(int id, UpdateProductDto);// false = not found
    Task<bool> DeleteProductAsync(int id);                  // false = not found
}

public class ProductService : IProductService
{
    private readonly AppDbContext _context;
    private readonly IAuditService _auditService;

    public ProductService(AppDbContext context, IAuditService auditService)
    {
        _context = context;
        _auditService = auditService;
    }
}
```

## Validation Patterns

**Input Validation** → `ArgumentException`
| Validation Type | Example |
|---|---|
| Required | `if (string.IsNullOrWhiteSpace(dto.Name)) throw new ArgumentException("Name required")` |
| Length | `if (dto.Name.Length > 200) throw new ArgumentException("Name max 200 chars")` |
| Range | `if (dto.Price <= 0) throw new ArgumentException("Price must be > 0")` |
| Format | `if (!IsValidEmail(dto.Email)) throw new ArgumentException("Invalid email")` |
| Collection | `if (!dto.Items.Any()) throw new ArgumentException("At least one item required")` |

**Business Rules** → `InvalidOperationException`
```csharp
// Duplicate check
if (await _context.Products.AnyAsync(p => p.Sku == dto.Sku))
    throw new InvalidOperationException($"SKU '{dto.Sku}' already exists");

// State check
var category = await _context.Categories.FindAsync(dto.CategoryId);
if (category != null && !category.IsActive)
    throw new InvalidOperationException("Cannot add products to inactive category");
```

## Return Value Patterns

| Operation | Return Type | Not Found | Validation Error | Example |
|---|---|---|---|---|
| GET | `Task<EntityDto?>` | return `null` | throw | `GetProductAsync(int id)` |
| POST | `Task<EntityDto>` | N/A | throw | `CreateProductAsync(dto)` |
| PUT | `Task<bool>` | return `false` | throw | `UpdateProductAsync(id, dto)` |
| DELETE | `Task<bool>` | return `false` | throw | `DeleteProductAsync(id)` |

```csharp
// GET - return null for not found
public async Task<ProductDto?> GetProductAsync(int id)
{
    var product = await _context.Products.FindAsync(id);
    return product != null ? MapToDto(product) : null;
}

// POST - throw on validation error
public async Task<ProductDto> CreateProductAsync(CreateProductDto dto)
{
    if (string.IsNullOrWhiteSpace(dto.Name))
        throw new ArgumentException("Name required");

    var product = new Product { Name = dto.Name, Price = dto.Price };
    _context.Products.Add(product);
    await _context.SaveChangesAsync();
    return MapToDto(product);
}

// PUT - return false for not found, throw on validation error
public async Task<bool> UpdateProductAsync(int id, UpdateProductDto dto)
{
    var product = await _context.Products.FindAsync(id);
    if (product == null) return false;

    if (dto.Price <= 0) throw new ArgumentException("Price must be > 0");

    product.Name = dto.Name;
    product.Price = dto.Price;
    await _context.SaveChangesAsync();
    return true;
}

// DELETE - return false for not found, throw on business rule violation
public async Task<bool> DeleteProductAsync(int id)
{
    var product = await _context.Products.FindAsync(id);
    if (product == null) return false;

    if (await _context.Orders.AnyAsync(o => o.ProductId == id))
        throw new InvalidOperationException("Cannot delete product with orders");

    _context.Products.Remove(product);
    await _context.SaveChangesAsync();
    return true;
}
```

## Data Access Patterns

**Direct DbContext** - Simple cases:
```csharp
public async Task<ProductDto?> GetProductAsync(int id)
{
    var product = await _context.Products.Include(p => p.Category).FindAsync(id);
    return product != null ? MapToDto(product) : null;
}
```

**Query Methods** - For reusability:
```csharp
private IQueryable<Product> GetProductsQuery(bool includeInactive = false)
{
    var query = _context.Products.Include(p => p.Category);
    return includeInactive ? query : query.Where(p => p.IsActive);
}

public async Task<IEnumerable<ProductDto>> GetProductsAsync(string? category = null)
{
    var query = GetProductsQuery();
    if (!string.IsNullOrEmpty(category))
        query = query.Where(p => p.Category.Name == category);

    return (await query.OrderBy(p => p.Name).ToListAsync()).Select(MapToDto);
}
```

**Let Database Exceptions Bubble** - Don't catch SaveChangesAsync failures:
```csharp
_context.Products.Add(product);
await _context.SaveChangesAsync(); // Let exceptions bubble to middleware
```

## Cross-Service Communication

Inject other services via constructor, use for business logic, apply graceful degradation for non-critical operations:

```csharp
public class OrderService : IOrderService
{
    private readonly IProductService _productService;
    private readonly IEmailService _emailService;

    public async Task<OrderDto> CreateOrderAsync(CreateOrderDto dto)
    {
        var product = await _productService.GetProductAsync(dto.ProductId);
        if (product == null) throw new ArgumentException("Product not found");
        if (!product.IsAvailable) throw new InvalidOperationException("Product unavailable");

        var order = new Order { ProductId = dto.ProductId };
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();

        // Non-critical email - don't fail order creation
        try { await _emailService.SendOrderConfirmationAsync(order.Id); }
        catch (Exception ex) { await _auditService.LogAsync("Email failed", ex); }

        return MapToDto(order);
    }
}
```

**Avoid circular dependencies**: Extract shared logic to third service instead of A→B and B→A.

## Mapping

```csharp
// Manual mapping - simple and explicit
private ProductDto MapToDto(Product p) => new ProductDto
{
    Id = p.Id,
    Name = p.Name,
    Price = p.Price,
    CategoryName = p.Category?.Name,
    IsAvailable = p.Quantity > 0
};

// Collections
return (await _context.Products.ToListAsync()).Select(MapToDto);
```

## Audit Logging

Log significant business operations (create, update, delete):

```csharp
public async Task<ProductDto> CreateProductAsync(CreateProductDto dto)
{
    var product = new Product { Name = dto.Name, Price = dto.Price };
    _context.Products.Add(product);
    await _context.SaveChangesAsync();

    await _auditService.LogAsync("CreateProduct", "Product", product.Id,
        oldValues: null, newValues: new { product.Name, product.Price });

    return MapToDto(product);
}

public async Task<bool> UpdateProductAsync(int id, UpdateProductDto dto)
{
    var product = await _context.Products.FindAsync(id);
    if (product == null) return false;

    var oldValues = new { product.Name, product.Price };
    product.Name = dto.Name;
    product.Price = dto.Price;
    await _context.SaveChangesAsync();

    await _auditService.LogAsync("UpdateProduct", "Product", id, oldValues,
        newValues: new { product.Name, product.Price });

    return true;
}
```

## External Services

**Non-Critical** (email, notifications) - Catch and log, don't fail main operation:
```csharp
var user = new User { Email = dto.Email };
_context.Users.Add(user);
await _context.SaveChangesAsync();

try { await _emailService.SendWelcomeEmailAsync(user.Email); }
catch (Exception ex)
{
    await _auditService.LogAsync("Welcome email failed", ex, user.Id);
    // Don't throw - registration succeeded
}
```

**Critical** (password reset, payment) - Log and re-throw:
```csharp
user.PasswordResetToken = GenerateResetToken();
await _context.SaveChangesAsync();

try { await _emailService.SendPasswordResetAsync(user.Email, token); }
catch (Exception ex)
{
    await _auditService.LogAsync("Password reset email failed", ex, user.Id);
    throw; // User must know email failed
}
```

**API Calls** - Graceful degradation when possible:
```csharp
try
{
    var response = await _httpClient.PostAsJsonAsync(url, address);
    return await response.Content.ReadFromJsonAsync<AddressDto>() ?? address;
}
catch (HttpRequestException ex)
{
    await _auditService.LogAsync("Address validation unavailable", ex);
    return address; // Fall back to unvalidated
}
```

## Transactions

**Simple** - Multiple changes in single SaveChangesAsync are atomic:
```csharp
var order = new Order { ProductId = dto.ProductId };
_context.Orders.Add(order);

var product = await _context.Products.FindAsync(dto.ProductId);
product.Quantity -= dto.Quantity;

await _context.SaveChangesAsync(); // All or nothing
```

**Explicit** - When spanning external services:
```csharp
using var transaction = await _context.Database.BeginTransactionAsync();
try
{
    var order = new Order { Total = dto.Total };
    _context.Orders.Add(order);
    await _context.SaveChangesAsync();

    var paymentResult = await _paymentService.ChargeAsync(dto.Token, order.Total);
    if (!paymentResult.Success)
        throw new InvalidOperationException($"Payment failed: {paymentResult.Error}");

    order.PaymentId = paymentResult.PaymentId;
    await _context.SaveChangesAsync();
    await transaction.CommitAsync();

    return MapToDto(order);
}
catch { await transaction.RollbackAsync(); throw; }
```

## Configuration

**Direct injection**:
```csharp
public EmailService(IConfiguration config)
{
    _apiKey = config["Email:ApiKey"] ?? throw new InvalidOperationException("API key required");
}
```

**Strongly-typed** (preferred):
```csharp
// Program.cs
services.Configure<EmailSettings>(configuration.GetSection("Email"));

// Service
public EmailService(IOptions<EmailSettings> settings) => _settings = settings.Value;
```

## Testing

Inject all dependencies for easy mocking:
```csharp
public class ProductService : IProductService
{
    private readonly AppDbContext _context;
    private readonly IAuditService _auditService;

    public ProductService(AppDbContext context, IAuditService auditService)
    {
        _context = context;
        _auditService = auditService;
    }
}

// Unit test
var mockContext = new Mock<AppDbContext>();
var mockAudit = new Mock<IAuditService>();
var service = new ProductService(mockContext.Object, mockAudit.Object);
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|---|---|---|
| Catch and swallow exceptions | Hides errors from users | Let exceptions bubble to middleware |
| Business logic in controllers | Violates separation of concerns | Move ALL logic to services |
| `new` dependencies in services | Hard to test, tight coupling | Use constructor injection |
| Return bool on validation errors | Caller doesn't know what failed | Throw descriptive exceptions |
| Circular service dependencies | Runtime errors | Extract shared logic to third service |
