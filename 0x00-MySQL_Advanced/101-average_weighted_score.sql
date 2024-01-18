-- Create stored procedure ComputeAverageWeightedScoreForUsers

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    SET average_score = (
        SELECT COALESCE(SUM(corrections.score * projects.weight) / SUM(projects.weight), 0)
        FROM corrections
        INNER JOIN projects ON projects.id = corrections.project_id
        WHERE corrections.user_id = users.id
    );
END;
//
DELIMITER ;
