# Creating Element Hierarchies in PI Web API

This guide shows two methods for creating element hierarchies in PI Asset Framework:

1. **Direct Element Creation** - Using `create_element()` methods
2. **OMF-based Creation** - Using OMF (OSIsoft Message Format)

## Method 1: Direct Element Creation

### When to Use
- Creating custom hierarchies with specific structure
- Adding elements to existing AF databases
- Need full control over element placement
- Working with AF templates

### Code Example

```python
from pi_web_sdk import PIWebAPIClient, PIWebAPIConfig

# Setup client
config = PIWebAPIConfig(
    base_url="https://your-server/piwebapi",
    username="user",
    password="pass",
    verify_ssl=False
)
client = PIWebAPIClient(config)

# Get database
servers = client.asset_server.list()
dbs = client.asset_server.get_databases(servers["Items"][0]["WebId"])
db_web_id = dbs["Items"][0]["WebId"]

# Create root element in database
plant = client.asset_database.create_element(db_web_id, {
    "Name": "Plant1",
    "Description": "Manufacturing plant"
})
plant_web_id = plant["WebId"]

# Create child elements
area = client.element.create_element(plant_web_id, {
    "Name": "Area1",
    "Description": "Production area"
})

line = client.element.create_element(area["WebId"], {
    "Name": "Line1",
    "Description": "Assembly line"
})

sensor = client.element.create_element(line["WebId"], {
    "Name": "TempSensor1",
    "Description": "Temperature sensor"
})

# Add attributes to sensor
client.element.create_attribute(sensor["WebId"], {
    "Name": "Temperature",
    "Type": "Double",
    "Description": "Current temperature"
})
```

### Pros
- ✅ Works with existing AF templates
- ✅ Integrates seamlessly with existing AF structure
- ✅ Fine-grained control over each element
- ✅ Can add complex attributes and references
- ✅ Immediate visibility in PI System Explorer

### Cons
- ❌ Requires one API call per element (can be slow for large hierarchies)
- ❌ More verbose code for deep hierarchies
- ❌ Manual tracking of WebIds for parent-child relationships

## Method 2: OMF-based Creation

### When to Use
- Bulk creation of many elements
- Creating data collection structures (containers + streams)
- Need to create types and instances together
- Time-series data ingestion with hierarchy

### Code Example

```python
from pi_web_sdk import PIWebAPIClient, PIWebAPIConfig
from pi_web_sdk.omf import OMFManager

# Setup
client = PIWebAPIClient(config)
servers = client.data_server.list()
manager = OMFManager(client, servers["Items"][0]["WebId"])

# Method 2a: Create from paths
paths = [
    "Plant1/Area1/Line1/Sensor1",
    "Plant1/Area1/Line1/Sensor2",
    "Plant1/Area2/Line2/Sensor3",
]

results = manager.create_hierarchy_from_paths(
    paths=paths,
    root_type_id="ContainerType",
    leaf_type_id="SensorType",
    create_types=True  # Creates OMF types automatically
)

# Method 2b: Create industrial hierarchy
results = manager.create_industrial_hierarchy(
    plants=["PlantA", "PlantB"],
    units_per_plant={
        "PlantA": ["Unit1", "Unit2"],
        "PlantB": ["Unit3", "Unit4"]
    },
    sensors_per_unit={
        "Unit1": ["Temp1", "Press1"],
        "Unit2": ["Flow1", "Level1"],
        "Unit3": ["Temp2", "Press2"],
        "Unit4": ["Flow2", "Level2"]
    },
    create_types=True
)
```

### Pros
- ✅ Fast bulk creation (one API call for many elements)
- ✅ Automatic type creation
- ✅ Great for time-series data structures
- ✅ Less code for complex hierarchies
- ✅ Built-in validation

### Cons
- ❌ Less control over individual elements
- ❌ May not integrate with existing AF templates
- ❌ Different type structure than traditional AF elements
- ❌ Primarily designed for PI Data Archive, not AF

## Comparison Table

| Feature | Direct Element Creation | OMF-based Creation |
|---------|------------------------|-------------------|
| **Speed (100 elements)** | ~100 API calls | ~2-3 API calls |
| **AF Template Support** | ✅ Full | ❌ Limited |
| **Custom Attributes** | ✅ Full control | ✅ Via properties |
| **Existing DB Integration** | ✅ Seamless | ⚠️ Separate structure |
| **Learning Curve** | Easy | Moderate |
| **Best For** | AF hierarchies | Data ingestion |

## Example Use Cases

### Use Direct Creation When:

1. **Extending Existing AF Structure**
   ```python
   # Add new area to existing plant
   existing_plant = client.element.get_by_path(r"\\AF_SERVER\DB\PlantA")
   new_area = client.element.create_element(existing_plant["WebId"], {
       "Name": "NewArea",
       "TemplateName": "AreaTemplate"  # Use existing template
   })
   ```

2. **Creating Equipment with Complex Attributes**
   ```python
   pump = client.asset_database.create_element(db_web_id, {
       "Name": "Pump123",
       "TemplateName": "PumpTemplate"
   })
   # Template auto-creates attributes based on definition
   ```

3. **Small to Medium Hierarchies** (< 50 elements)

### Use OMF Creation When:

1. **Bulk Data Collection Setup**
   ```python
   # Create 1000s of sensor streams quickly
   paths = [f"Field/Well_{i}/Sensor_{j}"
            for i in range(100) for j in range(10)]
   manager.create_hierarchy_from_paths(paths, ...)
   ```

2. **Standardized Hierarchies**
   ```python
   # Create identical structure across multiple plants
   for plant in ["PlantA", "PlantB", "PlantC"]:
       manager.create_industrial_hierarchy(
           plants=[plant],
           units_per_plant={plant: ["Unit1", "Unit2"]},
           ...
       )
   ```

3. **Time-Series Data Ingestion**
   ```python
   # Create container and start sending data
   manager.create_container(container)
   manager.send_time_series_data(data)
   ```

## Running the Examples

Both example files are available:

```bash
# Direct element creation examples
python examples/create_element_hierarchy.py

# OMF-based creation examples
python examples/create_hierarchy.py
```

## Running the Tests

```bash
# Test direct element creation
pytest tests/test_element_creation_live.py -v
pytest tests/test_element_hierarchy_creation_live.py -v

# Test OMF hierarchy creation
pytest tests/test_omf_hierarchy_live.py -v

# Run all hierarchy tests
pytest tests/test_*hierarchy*.py tests/test_element*.py -v
```

## Recommendations

### For Production AF Systems
Use **Direct Element Creation** because:
- Better integration with existing AF structure
- Works with AF templates and references
- More familiar to AF administrators
- Better visibility in PI System Explorer

### For Data Collection/IoT
Use **OMF Creation** because:
- Faster for large-scale deployments
- Built for time-series data
- Easier programmatic management
- Better for cloud/edge scenarios

## Need Help?

- Check the examples in `examples/` directory
- Run live tests to see working code: `pytest tests/test_*live.py -v -s`
- See [CLAUDE.md](../CLAUDE.md) for development guidelines
