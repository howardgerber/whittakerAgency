# Claude Code Session Configuration

## Session Startup Protocol

### 1. Auto-Read Documentation
At the beginning of each session, automatically read these files to get up to speed:
- `README.md` - Project overview and setup instructions
- `docs/architecture/exception-handling-pattern.md` - **CRITICAL**: Exception handling architecture
- `docs/architecture/service-layer-patterns.md` - Service design patterns
- `docs/architecture/project-structure.md` - Project organization and conventions
- `frontend/src/utils/validation.ts` - **MANDATORY**: Shared validation rules
- `frontend/src/utils/formatters.ts` - **MANDATORY**: Shared formatting functions
- Current git status to understand recent changes

### 2. Architecture Patterns to Follow

This project follows specific architecture patterns documented in the `docs/architecture/` folder:

#### Shared Validation & Formatting (MANDATORY)
- **ALWAYS check `frontend/src/utils/validation.ts` FIRST** before writing any validation logic
- **ALWAYS check `frontend/src/utils/formatters.ts` FIRST** before writing any formatting logic
- **If validation/formatting doesn't exist in shared utils:**
  1. STOP and ask the user: "Should this validation/formatting be added to shared utils or kept local?"
  2. Discuss whether it's reusable across forms (shared) or form-specific (local)
  3. Only proceed after user confirms the approach
- **Import from shared utils:**
  ```typescript
  import { ValidationRules } from '@/utils/validation'
  import { formatPhoneNumber, formatCurrency } from '@/utils/formatters'
  ```
- **NEVER duplicate validation or formatting logic across components**
- **Examples of shared validation:** phone, email, VIN, full name, dates, vehicle year
- **Examples of shared formatting:** phone numbers, currency, VIN, vehicle text

#### Exception Handling (CRITICAL)
- **Controllers must be thin** - NO business logic, NO try-catch blocks
- **Services contain all business logic** - throw meaningful, typed exceptions
- **GlobalExceptionMiddleware handles all exceptions** - centralized logging and status mapping
- **Exception types**:
  - `ArgumentException` → 400 Bad Request (validation errors)
  - `InvalidOperationException` → 409 Conflict (business rule violations)
  - `KeyNotFoundException` → 404 Not Found
  - All others → 500 Internal Server Error
- Services return null/false for "not found", throw exceptions for errors
- All exceptions bubble to GlobalExceptionMiddleware for logging and response

#### Service Layer
- ALL business logic belongs in services
- Validate input and throw `ArgumentException` with clear messages
- Enforce business rules and throw `InvalidOperationException`
- Let database exceptions bubble up naturally
- Use graceful degradation for non-critical operations (email, etc.)
- NEVER catch exceptions just to log and return false/null

#### Controller Layer
- Extract data from HTTP request
- Call service methods
- Check for null/false return values explicitly
- Return appropriate HTTP responses
- **DO NOT**: Add business logic, validation, or try-catch blocks

### 3. Documentation Standards

#### Location Convention
- **New documentation**: Always create in `docs/` folder
- **Updates to existing docs**: Update in current location
- **Architecture docs**: `docs/architecture/` - patterns and design decisions
- **API docs**: `docs/api/` - endpoint documentation
- **Database docs**: `docs/database/` - schema and migrations
- **Deployment docs**: `docs/deployment/` - deployment guides
- **Session logs**: `docs/sessions/` - detailed work history

#### File Naming Convention
- Use kebab-case: `feature-name.md`
- Include dates for session-specific docs: `2025-08-28-session-notes.md`
- Use system date for all date-based documentation filenames
- Prefix with type when relevant: `api-endpoints.md`, `guide-setup.md`

### 4. Development Workflow

#### Before Starting Work
1. Check git status and recent commits
2. Read documentation to understand current state
3. Ask about priorities if multiple tasks are possible

#### During Work
- Use TodoWrite tool proactively for complex multi-step tasks
- Create documentation as you go, not as an afterthought
- Put new docs in `docs/` folder from the start
- Follow established patterns from architecture docs

#### After Completing Work
1. Update or create daily session file: `docs/sessions/YYYY-MM-DD-descriptive-summary.md`
2. Update relevant documentation if patterns changed
3. Commit all changes including documentation
4. Provide summary of what was accomplished

### 5. Code Quality Standards

#### Follow Architecture Patterns
- Check `docs/architecture/exception-handling-pattern.md` before writing exception handling
- Check `docs/architecture/service-layer-patterns.md` before creating services
- Check `docs/architecture/project-structure.md` for naming and organization

#### Dependency Injection
- Always inject dependencies via constructor
- Never create dependencies inside services/controllers
- Use appropriate service lifetime (Scoped, Singleton, Transient)

#### Testing
- Unit tests should expect exceptions to be thrown (not caught by controllers)
- Integration tests should expect GlobalExceptionMiddleware error format
- Keep services testable with dependency injection

### 6. Communication Preferences

#### When to Use TodoWrite
- Multi-step tasks (3+ distinct steps)
- Complex implementations requiring planning
- When user provides multiple tasks
- NOT for single, straightforward tasks

#### Response Style
- Be concise and direct
- Avoid unnecessary explanations unless requested
- Focus on the specific task at hand
- Use the tools available effectively

### 7. Git Workflow

#### Commit Messages
- Use descriptive commit messages
- Include Claude Code attribution
- Group related changes into logical commits
- Update documentation in same commit when possible

#### Branch Naming
```
feature/feature-name
bugfix/issue-description
hotfix/critical-fix
refactor/area-of-refactoring
```

### 8. Key Architectural Rules

#### Controllers
```csharp
// ✅ GOOD: Thin controller, no try-catch
[HttpPost]
public async Task<ActionResult<ProductDto>> CreateProduct(CreateProductDto dto)
{
    var product = await _productService.CreateProductAsync(dto);
    return CreatedAtAction(nameof(GetProduct), new { id = product.Id }, product);
}

// ❌ BAD: Try-catch in controller
[HttpPost]
public async Task<ActionResult<ProductDto>> CreateProduct(CreateProductDto dto)
{
    try
    {
        var product = await _productService.CreateProductAsync(dto);
        return CreatedAtAction(nameof(GetProduct), new { id = product.Id }, product);
    }
    catch (ArgumentException ex)
    {
        return BadRequest(ex.Message); // ❌ Middleware does this
    }
}
```

#### Services
```csharp
// ✅ GOOD: Throw meaningful exceptions
public async Task<ProductDto> CreateProductAsync(CreateProductDto dto)
{
    if (string.IsNullOrWhiteSpace(dto.Name))
    {
        throw new ArgumentException("Product name is required");
    }

    var product = new Product { Name = dto.Name };
    _context.Products.Add(product);
    await _context.SaveChangesAsync(); // Let exceptions bubble

    return MapToDto(product);
}

// ❌ BAD: Catch and swallow exceptions
public async Task<ProductDto?> CreateProductAsync(CreateProductDto dto)
{
    try
    {
        var product = new Product { Name = dto.Name };
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        return MapToDto(product);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error creating product");
        return null; // ❌ Hides errors from user
    }
}
```

### 9. When to Ask vs. Proceed

**Ask the user when:**
- Architecture patterns are unclear for the specific scenario
- Multiple valid approaches exist
- Significant refactoring is needed
- Breaking changes are involved

**Proceed without asking when:**
- Following established patterns from architecture docs
- Fixing bugs that violate documented patterns
- Adding features that follow existing examples
- Writing tests for new functionality

### 10. Session Goals

- Be proactive with documentation
- Follow established architecture patterns strictly
- Use available tools effectively
- Maintain code quality and consistency
- Deliver working, well-documented features
- Keep controllers thin and services focused
- Let exceptions bubble to GlobalExceptionMiddleware

#### Entity Framework Migration Protocol
**🚨 CRITICAL: Always follow this exact sequence when creating migrations**

1. **Before Creating Migration:**
   ```bash
   git pull  # Ensure you have latest migrations
   git status  # Check for uncommitted changes
   ```

2. **Create Migration:**
   ```bash
   cd SageSteppeApi
   dotnet ef migrations add MigrationName --context SageSteppeDbContext
   ```

3. **Apply Migration IMMEDIATELY:**
   ```bash
   dotnet ef database update --context SageSteppeDbContext
   ```
   - ✅ If successful: Proceed to step 4
   - ❌ If failed: Fix the migration NOW before committing

4. **Test the Changes:**
   ```bash
   dotnet test  # Run backend tests
   ```

5. **Only Then Commit:**
   ```bash
   git add .
   git commit -m "Add migration: MigrationName"
   git push
   ```

**Why This Matters:**
- Migrations created but not applied create database/code mismatches
- Uncommitted migrations cause sync issues between sessions
- Failed migrations in production are extremely difficult to fix
- MariaDB handles check constraints differently than SQL Server

**Special Considerations for MariaDB:**
- Always check if constraints exist before dropping them
- Include data migrations when changing constraints
- Test constraint changes with existing data
- Use conditional SQL for MariaDB-specific operations

**Never:**
- Create a migration and commit without applying it
- Create multiple migrations without applying each one
- Modify a migration after it's been pushed to git
- Use `--force` flag on migrations in production

## Quick Reference

### Exception Handling Flow
1. Service validates input → throws `ArgumentException`
2. Service checks business rules → throws `InvalidOperationException`
3. Service performs data access → lets database exceptions bubble
4. Controller calls service → lets all exceptions bubble
5. GlobalExceptionMiddleware catches → logs to SystemLog → returns appropriate HTTP status

### When to Throw vs Return Null/False
- **Throw ArgumentException**: Invalid input (empty string, negative price, etc.)
- **Throw InvalidOperationException**: Business rule violation (duplicate SKU, inactive category, etc.)
- **Return null**: Entity not found in GET operation
- **Return false**: Entity not found in UPDATE/DELETE operation
- **NEVER**: Catch exceptions to return null/false

### Service Method Patterns
- **GET**: Return `Task<EntityDto?>` - null if not found
- **POST**: Return `Task<EntityDto>` - throw on validation error
- **PUT**: Return `Task<bool>` - false if not found, throw on validation error
- **DELETE**: Return `Task<bool>` - false if not found, throw on business rule violation

## Important Reminders

- **NO try-catch in controllers** - GlobalExceptionMiddleware handles all exceptions
- **NO business logic in controllers** - All logic belongs in services
- **NO logger in controllers** - GlobalExceptionMiddleware logs everything
- **Services throw exceptions** - Don't catch and swallow
- **Read architecture docs** - Before writing exception handling or services
- **Update session docs** - After completing work
