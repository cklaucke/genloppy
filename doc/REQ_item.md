# R-ITEM-001: Provide log entry specific item classes #
*genloppy* SHALL provide log entry specific item classes:
-   BaseItem
-   PackageItem
-   MergeItem
-   UnmergeItem
-   SyncItem

# R-ITEM-002: BaseItem #
*BaseItem* SHALL consist of
-   a timestamp (seconds since 1970-01-01 00:00:00 UTC)

# R-ITEM-003: PackageItem #
*PackageItem* SHALL inherit *BaseItem* and SHALL additionally consist of
-   atom name
-   atom version

# R-ITEM-004: MergeItem #
*MergeItem* SHALL inherit *PackageItem* and SHALL additionally consist of
-   a timestamp that indicates the end of the merge operation

The inherited *BaseItem*'s timestamp indicates the begin of the merge operation.

# R-ITEM-005: UnmergeItem #
*MergeItem* SHALL inherit *PackageItem*.

The inherited *BaseItem*'s timestamp indicates the end of the unmerge operation.

# R-ITEM-006: SyncItem #
*SyncItem* SHALL inherit *BaseItem* and SHALL additionally consist of
-   repository name

The inherited *BaseItem*'s timestamp indicates the end of the sync operation.
