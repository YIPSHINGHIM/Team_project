create TABLE Item(
  S_ID int not NULL,
  Dish VARCHAR(20) NOT NULL,
  Price FLOAT not NULL,
  Is_Available INT NOT NULL,
  PRIMARY KEY (S_ID)
  );
  
-- @author : Harveen Chada

create TABLE MenuTraits(
  ID int not NULL,
  spiciness int not null,
  hasBeef int,
  hasChicken int,
  hasPork int,
  hasMutton int,
  hasFish int,
  hasGluten int,
  hasEggs int,
  hasSoy int,
  hasDairy int,
  hasNuts int,
  hasAlcohol int,
  calories int,
  PRIMARY KEY (ID)
  );