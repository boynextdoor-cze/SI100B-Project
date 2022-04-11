## Specification for client side components

### Overlay

This API provides control over the gray overlay, which indicating the refresh is on going.

#### Show overlay
```javascript
    this.$emit("overlay", true);
```

#### Hide overlay

```javascript
    this.$emit("overlay", false);
```

### Remarks ###
- the Overlay API may not behaviour as you wish. it works as follows:
  - There is a sentinel integer i indicating if the overlay is on.
    When it's positive, the overlay is on; 
    When it's 0, the overlay is off.
  - When the `$emit("overlay", true)` is called, i increased by 1.
  - When the `$emit("overlay", true)` is called, i decresed by 1.