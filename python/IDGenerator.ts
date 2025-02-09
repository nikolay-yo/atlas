class IDGenerator {
  private static current: number = 1;
  private static ids: { [key: number]: boolean } = {};
  private static maxID: number = 100;

  // Initialize IDs
  static {
    for (let index = 0; index < IDGenerator.maxID; index++) {
      IDGenerator.ids[index + 1] = false;
    }
  }

  private static _next(): boolean {
    if (IDGenerator.current === -1) {
      for (let index = 1; index <= IDGenerator.maxID; index++) {
        if (!IDGenerator.ids[index]) {
          IDGenerator.current = index;
          return true;
        }
      }
    } else {
      for (let index = IDGenerator.current; index < IDGenerator.maxID; index++) {
        if (!IDGenerator.ids[index + 1]) {
          IDGenerator.current = index + 1;
          return true;
        }
      }
      for (let index = 1; index < IDGenerator.current; index++) {
        if (!IDGenerator.ids[index]) {
          IDGenerator.current = index;
          return true;
        }
      }
      IDGenerator.current = -1;
      return false;
    }
    return false;
  }

  public static GetNext(): number {
    if (IDGenerator.current !== -1) {
      const newId = IDGenerator.current;
      IDGenerator.ids[newId] = true;
      IDGenerator._next();
      return newId;
    } else {
      IDGenerator._next();
      if (IDGenerator.current === -1) {
        return -1;
      }
      const newId = IDGenerator.current;
      IDGenerator.ids[newId] = true;
      IDGenerator._next();
      return newId;
    }
  }

  public static HasID(): boolean {
    for (let index = 1; index <= IDGenerator.maxID; index++) {
      if (!IDGenerator.ids[index]) {
        return true;
      }
    }
    return false;
  }

  public static DeleteByID(GenID: number): boolean {
    if (IDGenerator.ids[GenID]) {
      IDGenerator.ids[GenID] = false;
      return true;
    } else {
      return false;
    }
  }

  public static IncreaseLimitBy(additionIdNumbers: number): void {
    for (let index = IDGenerator.maxID; index < IDGenerator.maxID + additionIdNumbers; index++) {
      IDGenerator.ids[index + 1] = false;
    }
    IDGenerator.maxID += additionIdNumbers;
  }

  public static TestGenerator1(): void {
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("TakeId():", IDGenerator.GetNext());
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("TakeId():", IDGenerator.GetNext());
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("TakeId():", IDGenerator.GetNext());
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("ReleaseID(3)", IDGenerator.DeleteByID(3));
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("MoveToNextFreeID()", IDGenerator.GetNext());
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("ReleaseID(2)", IDGenerator.DeleteByID(2));
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("TakeId():", IDGenerator.GetNext());
    console.log("-----------------------");
    console.log("IDs", IDGenerator.ids);
    console.log("-----------------------");
    console.log("current : ", IDGenerator.current);
    console.log("-----------------------");
    console.log("HasFreeID()", IDGenerator.HasID());
    IDGenerator.IncreaseLimitBy(5);
  }
}

// Uncomment to run the test
// IDGenerator.TestGenerator1();
