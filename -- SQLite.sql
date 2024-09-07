-- SQLite
CREATE TRIGGER UpdateCalories
AFTER UPDATE ON Tracking
FOR EACH ROW
BEGIN
    UPDATE Tracking
    SET 
        TotalCaloriesConsumed = NEW.BreakfastCalories + NEW.LunchCalories + NEW.DinnerCalories + NEW.SnackCalories,
        RemainingCalories = DailyCalorieGoal - (NEW.BreakfastCalories + NEW.LunchCalories + NEW.DinnerCalories + NEW.SnackCalories)
    WHERE rowid = NEW.rowid;
END;

