# Project Structure and Organization

## Overview
Standard project structure, naming conventions, and organizational patterns.

## Directory Structure

```
ProjectName/
├── Controllers/              # API endpoints (thin, NO business logic)
├── Services/                 # ALL business logic
│   ├── Business/            # Domain services (Users/, Products/, Orders/)
│   ├── Infrastructure/      # Cross-cutting (Email/, Storage/, Logging/)
│   └── External/            # External APIs (Payment/, SMS/)
├── Models/                  # Database entities
├── DTOs/                    # Data Transfer Objects (Requests/, Responses/)
├── Data/                    # DbContext, Configurations/, Migrations/
├── Middleware/              # GlobalExceptionMiddleware, etc.
├── Utilities/               # ⭐ Shared utilities (Validation/, Formatting/, Constants/)
├── Tests/                   # Unit/, Integration/, Mocks/
└── docs/                    # Documentation

Frontend/
├── src/
│   ├── components/          # Reusable Vue components
│   ├── views/               # Page-level components
│   ├── services/            # API client
│   ├── utils/               # ⭐ Shared utilities (validation.js, formatting.js, constants.js)
│   ├── router/              # Routes
│   └── stores/              # Pinia stores
```

## Shared Code & Utilities (DRY Principle)

**Rule**: If code appears in 2+ places, extract it to a shared utility.

### Backend: Utilities/ Folder

```csharp
// Utilities/ValidationHelper.cs
public static class ValidationHelper
{
    public static bool IsValidEmail(string email) =>
        Regex.IsMatch(email, @"^[^@\s]+@[^@\s]+\.[^@\s]+$");
}

// Utilities/FormatHelper.cs
public static class FormatHelper
{
    public static string FormatPhone(string phone) =>
        phone?.Length == 10 ? $"({phone[..3]}) {phone[3..6]}-{phone[6..]}" : phone ?? "";
}

// Utilities/AppConstants.cs
public static class AppConstants
{
    public const int MaxProductNameLength = 200;
    public static class ErrorMessages
    {
        public const string InvalidEmail = "Invalid email address format";
    }
}

// Services use shared utilities
public class UserService : IUserService
{
    public async Task<UserDto> CreateUserAsync(CreateUserDto dto)
    {
        if (!ValidationHelper.IsValidEmail(dto.Email))
            throw new ArgumentException(AppConstants.ErrorMessages.InvalidEmail);
        // ...
    }
}
```

### Frontend: src/utils/ Folder

```javascript
// src/utils/validation.js
export const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

// src/utils/formatting.js
export const formatPhone = (phone) => {
  const cleaned = phone.replace(/\D/g, '');
  return cleaned.length === 10 ? `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}` : phone;
};

// src/utils/constants.js
export const ERROR_MESSAGES = {
  INVALID_EMAIL: 'Invalid email address format'
};

// Components import shared utilities
import { isValidEmail } from '@/utils/validation';
import { formatPhone } from '@/utils/formatting';
import { ERROR_MESSAGES } from '@/utils/constants';
```

### What to Share

| Type | Backend | Frontend |
|---|---|---|
| **Validation** | `ValidationHelper.cs` | `validation.js` |
| **Formatting** | `FormatHelper.cs` | `formatting.js` |
| **Constants** | `AppConstants.cs` | `constants.js` |
| **API Config** | `appsettings.json` | `api.js` |

### When to Extract

- Same regex/logic in 2+ services/components
- Common formatting (dates, currency, phone)
- Repeated error messages or constants
- Shared business rules (max lengths, price limits)

## Naming Conventions

| Element | Pattern | Examples |
|---|---|---|
| **Controllers** | Plural, PascalCase | `ProductsController.cs`, `UsersController.cs` |
| **Services (Interface)** | `I` + Singular | `IProductService.cs`, `IEmailService.cs` |
| **Services (Impl)** | Singular, PascalCase | `ProductService.cs`, `UserService.cs` |
| **Models** | Singular, PascalCase | `Product.cs`, `User.cs`, `Order.cs` |
| **DTOs** | Action/Purpose + Entity + `Dto` | `CreateProductDto.cs`, `ProductDto.cs` |
| **Tests** | Subject + `Tests` | `ProductServiceTests.cs` |
| **Methods** | PascalCase + `Async` | `GetProductAsync()`, `CreateOrderAsync()` |
| **Properties** | PascalCase | `ProductId`, `Name`, `Price` |
| **Private Fields** | `_` + camelCase | `_productService`, `_context`, `_logger` |
| **Local Variables** | camelCase | `productDto`, `userId`, `userName` |
| **Constants** | PascalCase | `MaxPageSize`, `DefaultCurrency` |

## Layer Responsibilities

| Layer | What It Does | What It DOESN'T Do |
|---|---|---|
| **Controllers** | Extract request data, call services, return responses | NO business logic, NO validation, NO try-catch |
| **Services** | Validation, business rules, data access, audit logging | NO HTTP concerns, NO presentation logic |
| **Data** | Entity definitions, DbContext, migrations | NO business logic |
| **DTOs** | Data contracts, validation attributes | NO business logic |

```csharp
// Controller - thin, no logic
[HttpGet("{id}")]
public async Task<ActionResult<ProductDto>> GetProduct(int id)
{
    var product = await _productService.GetProductAsync(id);
    return product == null ? NotFound() : Ok(product);
}

// Service - ALL business logic
public async Task<ProductDto> CreateProductAsync(CreateProductDto dto)
{
    if (string.IsNullOrWhiteSpace(dto.Name))
        throw new ArgumentException("Name required");

    var product = new Product { Name = dto.Name, Price = dto.Price };
    _context.Products.Add(product);
    await _context.SaveChangesAsync();
    return MapToDto(product);
}
```

## Dependency Injection

**Service Lifetimes:**
```csharp
// Scoped - per HTTP request (business services, DbContext)
services.AddScoped<IProductService, ProductService>();
services.AddScoped<IUserService, UserService>();

// Singleton - application lifetime (email, config)
services.AddSingleton<IEmailService, EmailService>();

// Transient - new instance every time (lightweight services)
services.AddTransient<IAuditService, AuditService>();

// Separate logging context (critical!)
services.AddDbContext<AppDbContext>(options => options.UseSqlServer(connStr));
services.AddDbContext<LoggingDbContext>(options => options.UseSqlServer(logConnStr));
```

**Constructor Injection:**
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
```

## Configuration

**appsettings.json structure:**
```json
{
  "ConnectionStrings": { "DefaultConnection": "...", "LoggingConnection": "..." },
  "AppSettings": { "FrontendUrl": "...", "ApiBaseUrl": "..." },
  "Email": { "ApiKey": "...", "FromAddress": "noreply@example.com" },
  "Jwt": { "SecretKey": "...", "Issuer": "...", "ExpirationMinutes": 60 }
}
```

**Usage:**
```csharp
// Direct: var url = _configuration["AppSettings:FrontendUrl"];

// Strongly-typed (preferred):
services.Configure<EmailSettings>(configuration.GetSection("Email"));
public EmailService(IOptions<EmailSettings> settings) => _settings = settings.Value;
```

## Database

**Entity Conventions:**
```csharp
public class Product
{
    public int Id { get; set; }                          // PK, auto-increment
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }             // Nullable = optional

    // Navigation properties
    public int CategoryId { get; set; }
    public Category Category { get; set; } = null!;
    public ICollection<OrderItem> OrderItems { get; set; } = new();
}
```

**Entity Configuration:**
```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.HasKey(p => p.Id);
        builder.Property(p => p.Name).IsRequired().HasMaxLength(200);
        builder.Property(p => p.Price).HasColumnType("decimal(18,2)");
        builder.HasOne(p => p.Category).WithMany(c => c.Products).HasForeignKey(p => p.CategoryId);
        builder.HasIndex(p => p.Name);
    }
}
```

## Testing

**Unit Tests** - Mock dependencies:
```csharp
public class ProductServiceTests
{
    private readonly Mock<AppDbContext> _mockContext;
    private readonly ProductService _service;

    [Fact]
    public async Task CreateProduct_WithValidData_ShouldCreateProduct()
    {
        var dto = new CreateProductDto { Name = "Test", Price = 10 };
        var result = await _service.CreateProductAsync(dto);
        Assert.Equal("Test", result.Name);
    }

    [Fact]
    public async Task CreateProduct_WithEmptyName_ShouldThrowArgumentException()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.CreateProductAsync(new CreateProductDto { Name = "", Price = 10 }));
    }
}
```

**Integration Tests** - Test full stack with in-memory DB:
```csharp
public class ProductsIntegrationTests : IDisposable
{
    private readonly HttpClient _client;

    public ProductsIntegrationTests()
    {
        var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(b => b.ConfigureServices(s =>
                s.AddDbContext<AppDbContext>(o => o.UseInMemoryDatabase("TestDb"))));
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task POST_Products_WithValidData_ShouldReturn201()
    {
        var response = await _client.PostAsJsonAsync("/api/products",
            new CreateProductDto { Name = "Test", Price = 10 });
        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
    }
}
```

## Documentation Structure
```
docs/
├── architecture/     # exception-handling-pattern.md, service-layer-patterns.md, project-structure.md
├── api/             # endpoints.md, authentication.md
├── database/        # schema.md, migrations.md
├── deployment/      # production.md, docker.md
└── sessions/        # 2025-01-15-feature-implementation.md
```

## Git Workflow
**Branches**: `feature/name`, `bugfix/name`, `hotfix/name`, `refactor/name`

**Commits**: Descriptive messages
```
Add user authentication feature
Fix login validation bug
Update product service exception handling
```

## Code Organization

**File Size Guidelines:**
- Controllers: < 200 lines
- Services: < 500 lines (split if larger)
- Models: < 100 lines
- DTOs: < 50 lines

**Folder Depth**: Max 3-4 levels, group by domain not technical type (`Services/Business/Products/` not `Services/Products/Business/`)

**Avoid Regions**: Organize naturally, split files if needed

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|---|---|---|
| God objects | One service does everything | Split into focused services per domain |
| Circular dependencies | A→B and B→A | Extract shared logic to third service |
| Leaky abstractions | Service returns entities | Always return DTOs from services |
| New in services | `new EmailService()` | Use constructor injection |
