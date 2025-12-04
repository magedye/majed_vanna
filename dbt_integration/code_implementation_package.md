# Complete Implementation Package for Semantic Layer
## Code Files - Ready to Copy & Paste

This document contains all production-ready Python code files for the Semantic Layer implementation.

---

# FILE 1: base_metadata_provider.py

```python
# app/agent/semantic_tools/base_metadata_provider.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class MetadataProvider(ABC):
    """
    Abstract interface for any metadata provider source.
    
    This interface ensures all providers (Oracle, dbt, DataHub, Direct DB)
    have a consistent contract for metadata extraction.
    
    All providers must implement these methods:
    - get_tables(): Returns list of table names
    - get_columns(): Returns column information per table
    - get_relationships(): Returns foreign key relationships
    - get_hierarchy(): Optional - returns hierarchy information
    """

    @abstractmethod
    def get_tables(self) -> List[str]:
        """
        Returns list of table names from the metadata source.
        
        Returns:
            List[str]: Uppercase table names (e.g., ['ACCOUNTS', 'TRANSACTIONS'])
        """
        pass

    @abstractmethod
    def get_columns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Returns column information for each table.
        
        Returns:
            Dict mapping table names to list of column specifications.
            Example:
            {
                'ACCOUNTS': [
                    {'column': 'ACCOUNT_ID', 'type': 'NUMBER', 'nullable': False},
                    {'column': 'BALANCE', 'type': 'NUMBER', 'nullable': False}
                ],
                'TRANSACTIONS': [...]
            }
        """
        pass

    @abstractmethod
    def get_relationships(self) -> List[Dict[str, str]]:
        """
        Returns foreign key relationships between tables.
        
        Returns:
            List of relationship specifications.
            Example:
            [
                {
                    'table': 'TRANSACTIONS',
                    'column': 'ACCOUNT_ID',
                    'ref_table': 'ACCOUNTS',
                    'ref_column': 'ACCOUNT_ID'
                }
            ]
        """
        pass

    def get_hierarchy(self) -> List[Dict[str, str]]:
        """
        Optional: Returns parent-child hierarchy information.
        
        Override this method if your metadata source supports hierarchy.
        
        Returns:
            List of hierarchy specifications (empty list if not applicable)
        """
        return []
```

---

# FILE 2: provider_direct_db.py

```python
# app/agent/semantic_tools/provider_direct_db.py

import json
import os
from typing import List, Dict, Any
from .base_metadata_provider import MetadataProvider


class DirectDbMetadataProvider(MetadataProvider):
    """
    Provider that reads metadata from static JSON files.
    
    Useful for:
    - Offline development and testing
    - Backward compatibility with existing JSON metadata
    - Quick prototyping without database connection
    
    Expected file structure:
        metadata/
            ├── tables.json
            ├── columns.json
            └── relationships.json
    """

    def __init__(self, metadata_dir: str = "metadata"):
        """
        Initialize provider from JSON files.
        
        Args:
            metadata_dir: Directory containing metadata JSON files
        """
        self.metadata_dir = metadata_dir
        self.tables_data = self._load_json("tables.json", [])
        self.columns_data = self._load_json("columns.json", {})
        self.relationships_data = self._load_json("relationships.json", [])

    def _load_json(self, filename: str, default):
        """
        Safely load JSON file with fallback to default value.
        
        Args:
            filename: Name of JSON file to load
            default: Default value if file not found or invalid
        
        Returns:
            Loaded JSON data or default value
        """
        try:
            filepath = os.path.join(self.metadata_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Warning: {filename} not found, using empty default")
            return default
        except json.JSONDecodeError:
            print(f"⚠️  Warning: {filename} is not valid JSON")
            return default

    def get_tables(self) -> List[str]:
        """Returns list of tables from tables.json."""
        return self.tables_data

    def get_columns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Returns columns from columns.json."""
        return self.columns_data

    def get_relationships(self) -> List[Dict[str, str]]:
        """Returns relationships from relationships.json."""
        return self.relationships_data
```

---

# FILE 3: provider_oracle.py

```python
# app/agent/semantic_tools/provider_oracle.py

try:
    import oracledb
except ImportError:
    oracledb = None

from typing import Dict, List, Any
import os
from .base_metadata_provider import MetadataProvider


class OracleMetadataProvider(MetadataProvider):
    """
    Live metadata extractor for Oracle Database (12c/19c/21c+).
    
    Features:
    - Real-time schema extraction
    - Automatic relationship discovery via foreign keys
    - Support for current schema only
    - Uses python-oracledb in thin mode (no Instant Client required)
    
    Requirements:
        pip install oracledb
    """

    def __init__(self, dsn: str, user: str = None, password: str = None):
        """
        Initialize connection to Oracle database.
        
        Args:
            dsn: Connection string (host:port/service or tnsnames entry)
            user: Oracle username (from DB_ORACLE_USER env if not provided)
            password: Oracle password (from DB_ORACLE_PASSWORD env if not provided)
        
        Raises:
            ImportError: If oracledb library not installed
            Exception: If connection fails
        """
        if not oracledb:
            raise ImportError(
                "oracledb library is required. Install with: pip install oracledb"
            )
        
        user = user or os.getenv("DB_ORACLE_USER")
        password = password or os.getenv("DB_ORACLE_PASSWORD")
        
        if not user or not password:
            raise ValueError("Oracle username and password required")
        
        try:
            self.conn = oracledb.connect(user=user, password=password, dsn=dsn)
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to Oracle database: {dsn}")
        except Exception as e:
            raise Exception(f"Failed to connect to Oracle: {e}")

    def get_tables(self) -> List[str]:
        """
        Extract tables from current schema.
        
        Returns:
            List of uppercase table names
        """
        query = """
            SELECT table_name FROM user_tables 
            ORDER BY table_name
        """
        self.cursor.execute(query)
        tables = [row[0].upper() for row in self.cursor.fetchall()]
        print(f"✅ Extracted {len(tables)} tables from Oracle")
        return tables

    def get_columns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract column definitions for all tables.
        
        Returns:
            Dict mapping table names to column specifications
        """
        result = {}
        query = """
            SELECT table_name, column_name, data_type, nullable
            FROM user_tab_columns 
            ORDER BY table_name, column_id
        """
        self.cursor.execute(query)
        
        for table_name, column_name, data_type, nullable in self.cursor.fetchall():
            table_name = table_name.upper()
            result.setdefault(table_name, [])
            result[table_name].append({
                "column": column_name.upper(),
                "type": data_type,
                "nullable": nullable == "Y"
            })
        
        total_cols = sum(len(cols) for cols in result.values())
        print(f"✅ Extracted {total_cols} columns from {len(result)} tables")
        return result

    def get_relationships(self) -> List[Dict[str, str]]:
        """
        Extract foreign key relationships.
        
        Returns:
            List of foreign key relationship specifications
        """
        query = """
            SELECT 
                a.table_name,
                a.column_name,
                c_pk.table_name,
                b.column_name
            FROM user_cons_columns a
            JOIN user_constraints c ON 
                a.owner = c.owner AND a.constraint_name = c.constraint_name
            JOIN user_constraints c_pk ON 
                c.r_owner = c_pk.owner AND c.r_constraint_name = c_pk.constraint_name
            JOIN user_cons_columns b ON 
                c.r_constraint_name = b.constraint_name AND b.position = a.position
            WHERE c.constraint_type = 'R'
        """
        self.cursor.execute(query)
        
        result = []
        for child_table, child_col, parent_table, parent_col in self.cursor.fetchall():
            result.append({
                "table": child_table.upper(),
                "column": child_col.upper(),
                "ref_table": parent_table.upper(),
                "ref_column": parent_col.upper()
            })
        
        print(f"✅ Extracted {len(result)} relationships")
        return result

    def __del__(self):
        """Clean up database connection."""
        try:
            if self.conn:
                self.conn.close()
        except Exception:
            pass
```

---

# FILE 4: semantic_model_compiler.py

```python
# app/agent/semantic_tools/semantic_model_compiler.py

import yaml
import json
import os
from typing import Dict, Any
from datetime import datetime
from .base_metadata_provider import MetadataProvider


def compile_semantic_model_from_provider(
    provider: MetadataProvider,
    vocabulary: Dict[str, Any] = None,
    metrics: Dict[str, Any] = None,
    rules: Dict[str, Any] = None,
    intents: Dict[str, Any] = None,
    output: str = "semantic_model.yaml"
) -> str:
    """
    Orchestrate the semantic model compilation process.
    
    This is the central compiler that:
    1. Extracts metadata from any provider
    2. Merges with business rules (vocabulary, metrics, rules, intents)
    3. Generates unified semantic_model.yaml
    4. Validates output
    
    Args:
        provider: MetadataProvider instance (Oracle, dbt, DataHub, etc.)
        vocabulary: Domain vocabulary mappings (dict)
        metrics: Business metrics definitions (dict)
        rules: Business rules (dict)
        intents: User intent classifications (dict)
        output: Output file path
    
    Returns:
        Path to generated semantic_model.yaml
    
    Raises:
        ValueError: If compilation fails validation
    """
    
    print(f"\n🔄 Compiling semantic model using {provider.__class__.__name__}...")
    
    # Step 1: Extract metadata from provider
    tables = provider.get_tables()
    columns = provider.get_columns()
    relationships = provider.get_relationships()
    hierarchy = provider.get_hierarchy()
    
    # Step 2: Set defaults for optional config
    vocabulary = vocabulary or {}
    metrics = metrics or {}
    rules = rules or {}
    intents = intents or {}
    
    # Step 3: Build semantic model structure
    semantic_model = {
        "semantic_model": {
            "version": "2.0",
            "metadata": {
                "generated_by": f"Vanna Semantic Compiler ({provider.__class__.__name__})",
                "generated_at": datetime.now().isoformat(),
                "provider": provider.__class__.__name__
            },
            "schema": {
                "tables": tables,
                "columns": columns,
                "relationships": relationships,
                "hierarchy": hierarchy
            },
            "business_intelligence": {
                "vocabulary": vocabulary,
                "metrics": metrics,
                "rules": rules,
                "intents": intents
            }
        }
    }
    
    # Step 4: Validate semantic model
    _validate_semantic_model(semantic_model)
    
    # Step 5: Write to YAML
    with open(output, "w", encoding="utf-8") as f:
        yaml.dump(semantic_model, f, allow_unicode=True, sort_keys=False)
    
    # Step 6: Report success
    print(f"\n✅ Successfully generated '{output}'")
    print(f"   📊 Tables: {len(tables)}")
    print(f"   📋 Columns: {sum(len(c) for c in columns.values())}")
    print(f"   🔗 Relationships: {len(relationships)}")
    print(f"   📝 Vocabulary entries: {len(vocabulary)}")
    print(f"   📈 Metrics defined: {len(metrics)}")
    print(f"   ⚡ Rules defined: {len(rules)}")
    print(f"   🎯 Intents defined: {len(intents)}")
    
    return output


def _validate_semantic_model(model: Dict[str, Any]) -> None:
    """
    Validate semantic model structure.
    
    Args:
        model: Semantic model dictionary
    
    Raises:
        ValueError: If validation fails
    """
    
    try:
        sm = model.get("semantic_model", {})
        schema = sm.get("schema", {})
        
        # Validate structure
        assert "tables" in schema, "Missing 'tables' in schema"
        assert "columns" in schema, "Missing 'columns' in schema"
        assert isinstance(schema["tables"], list), "Tables must be list"
        assert isinstance(schema["columns"], dict), "Columns must be dict"
        
        # Validate columns reference tables
        for table in schema["columns"].keys():
            if table not in schema["tables"]:
                raise ValueError(f"Column table '{table}' not in tables list")
        
        # Validate relationships
        relationships = schema.get("relationships", [])
        for rel in relationships:
            if rel.get("table") not in schema["tables"]:
                raise ValueError(f"Relationship table '{rel.get('table')}' not found")
            if rel.get("ref_table") not in schema["tables"]:
                raise ValueError(f"Relationship ref_table '{rel.get('ref_table')}' not found")
        
        print("   ✓ Schema validation passed")
        
    except (AssertionError, ValueError) as e:
        raise ValueError(f"Semantic model validation failed: {e}")
```

---

# FILE 5: __init__.py (semantic_tools)

```python
# app/agent/semantic_tools/__init__.py

from .base_metadata_provider import MetadataProvider
from .provider_direct_db import DirectDbMetadataProvider
from .provider_oracle import OracleMetadataProvider
from .semantic_model_compiler import compile_semantic_model_from_provider

__all__ = [
    "MetadataProvider",
    "DirectDbMetadataProvider",
    "OracleMetadataProvider",
    "compile_semantic_model_from_provider"
]
```

---

# FILE 6: metadata.py (API Router)

```python
# app/api/metadata.py

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any
import os
import json
import yaml

from app.agent.semantic_tools.provider_direct_db import DirectDbMetadataProvider
from app.agent.semantic_tools.provider_oracle import OracleMetadataProvider
from app.agent.semantic_tools.semantic_model_compiler import compile_semantic_model_from_provider

router = APIRouter()

CONFIG_FILE = "metadata_config.json"


def get_active_provider():
    """
    Factory method to instantiate the correct metadata provider.
    
    Selection priority:
    1. Configuration file (persisted user choice via UI)
    2. Environment variable (METADATA_SOURCE)
    3. Default (direct)
    
    Supported sources: direct, oracle
    """
    source = os.getenv("METADATA_SOURCE", "direct")
    
    # Load persisted configuration if exists
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                source = config.get("source", source)
        except Exception:
            pass
    
    # Instantiate appropriate provider
    if source == "oracle":
        dsn = os.getenv("DB_ORACLE_DSN", "localhost:1521/orcl")
        try:
            return OracleMetadataProvider(dsn)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Oracle connection failed: {e}")
    
    # Default to direct DB
    return DirectDbMetadataProvider("metadata")


@router.get("/config", tags=["metadata"])
def get_config():
    """
    Get current metadata configuration.
    
    Returns:
        Dictionary with current source and settings
    """
    source = os.getenv("METADATA_SOURCE", "direct")
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"source": source}


@router.post("/config", tags=["metadata"])
def update_config(payload: Dict[str, Any] = Body(...)):
    """
    Update metadata configuration.
    
    Args:
        payload: Configuration dictionary with 'source' key
    
    Returns:
        Success confirmation with updated config
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(payload, f)
        return {"status": "updated", "config": payload}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables", tags=["metadata"])
def get_tables():
    """
    List all tables from active metadata source.
    
    Returns:
        List of table names
    """
    try:
        provider = get_active_provider()
        return {"tables": provider.get_tables()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/columns", tags=["metadata"])
def get_columns():
    """
    Get column definitions for all tables.
    
    Returns:
        Dict mapping table names to column specifications
    """
    try:
        provider = get_active_provider()
        return {"columns": provider.get_columns()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/relationships", tags=["metadata"])
def get_relationships():
    """
    Get table relationships and foreign keys.
    
    Returns:
        List of relationship specifications
    """
    try:
        provider = get_active_provider()
        return {"relationships": provider.get_relationships()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", tags=["metadata"])
def generate_semantic_model():
    """
    Generate semantic_model.yaml from current metadata source.
    
    This endpoint orchestrates the full compilation process:
    1. Extract metadata from active provider
    2. Load business configuration (vocabulary, metrics, rules, intents)
    3. Compile to semantic_model.yaml
    4. Validate output
    
    Returns:
        Success confirmation with file path
    """
    try:
        provider = get_active_provider()
        
        # Load business configuration files
        def load_config(path, is_json=False):
            try:
                if not os.path.exists(path):
                    return {} if is_json else {}
                
                with open(path, "r", encoding="utf-8") as f:
                    if is_json:
                        return json.load(f)
                    else:
                        return yaml.safe_load(f) or {}
            except Exception:
                return {}
        
        vocabulary = load_config("semantic/vocabulary.json", is_json=True)
        metrics = load_config("semantic/metrics.yaml", is_json=False)
        rules = load_config("semantic/rules.yaml", is_json=False)
        intents = load_config("semantic/intents.yaml", is_json=False)
        
        # Compile semantic model
        output_file = compile_semantic_model_from_provider(
            provider=provider,
            vocabulary=vocabulary,
            metrics=metrics,
            rules=rules,
            intents=intents,
            output="semantic_model.yaml"
        )
        
        return {
            "status": "success",
            "message": "Semantic model regenerated successfully",
            "file": output_file
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

# FILE 7: requirements.txt (additions)

```
# Add these to your existing requirements.txt

# Metadata extraction
oracledb>=1.0.0

# YAML processing
PyYAML>=6.0

# API
fastapi>=0.95.0
uvicorn>=0.21.0

# Database drivers (keep existing ones)

# Semantic layer optional
numpy>=1.24.0
pandas>=2.0.0
```

---

# FILE 8: .env (example)

```bash
# Metadata Provider Configuration
METADATA_SOURCE=direct              # Options: direct, oracle

# Oracle Connection (if using OracleMetadataProvider)
DB_ORACLE_DSN=hostname:1521/dbname
DB_ORACLE_USER=username
DB_ORACLE_PASSWORD=password

# Semantic Layer
SEMANTIC_MODEL_PATH=semantic_model.yaml
VOCABULARY_PATH=semantic/vocabulary.json
METRICS_PATH=semantic/metrics.yaml
RULES_PATH=semantic/rules.yaml
INTENTS_PATH=semantic/intents.yaml

# API
METADATA_API_ENABLED=true
SEMANTIC_API_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

---

# FILE 9: build_semantic_model.py (CLI tool)

```python
#!/usr/bin/env python3
# tools/build_semantic_model.py

import os
import json
import yaml
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agent.semantic_tools.provider_direct_db import DirectDbMetadataProvider
from app.agent.semantic_tools.provider_oracle import OracleMetadataProvider
from app.agent.semantic_tools.semantic_model_compiler import compile_semantic_model_from_provider

def main():
    """Build semantic model from configured metadata source."""
    
    # Get provider source
    source = os.getenv("METADATA_SOURCE", "direct")
    
    print(f"🚀 Building semantic model from: {source}")
    
    # Get provider
    if source == "oracle":
        dsn = os.getenv("DB_ORACLE_DSN")
        if not dsn:
            print("❌ Error: DB_ORACLE_DSN not configured")
            sys.exit(1)
        provider = OracleMetadataProvider(dsn)
    else:
        provider = DirectDbMetadataProvider("metadata")
    
    # Load business configuration
    def load_config(path):
        if not os.path.exists(path):
            return {}
        try:
            if path.endswith(".json"):
                with open(path) as f:
                    return json.load(f)
            else:
                with open(path) as f:
                    return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"⚠️  Warning loading {path}: {e}")
            return {}
    
    vocabulary = load_config("semantic/vocabulary.json")
    metrics = load_config("semantic/metrics.yaml")
    rules = load_config("semantic/rules.yaml")
    intents = load_config("semantic/intents.yaml")
    
    # Compile
    try:
        compile_semantic_model_from_provider(
            provider=provider,
            vocabulary=vocabulary,
            metrics=metrics,
            rules=rules,
            intents=intents,
            output="semantic_model.yaml"
        )
        print("\n✅ Semantic model built successfully!")
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

# SUMMARY

This package contains all production-ready code files needed for semantic layer integration.

**Files included:**
1. ✅ base_metadata_provider.py (Abstract interface)
2. ✅ provider_direct_db.py (Legacy JSON support)
3. ✅ provider_oracle.py (Live Oracle extraction)
4. ✅ semantic_model_compiler.py (Compilation engine)
5. ✅ __init__.py (Package initialization)
6. ✅ metadata.py (REST API)
7. ✅ requirements.txt (Dependencies)
8. ✅ .env (Configuration template)
9. ✅ build_semantic_model.py (CLI tool)

**Installation:**
1. Copy all Python files to appropriate directories
2. Update requirements.txt with new dependencies
3. Configure .env file
4. Run: `python tools/build_semantic_model.py`
5. Verify: `curl http://localhost:8000/api/metadata/config`

**Next steps:**
- Deploy configuration files (vocabulary.json, metrics.yaml, rules.yaml, intents.yaml)
- Set up metadata extraction from your Oracle database
- Integrate with Vanna Agent (no code changes needed)
- Deploy API and admin dashboard