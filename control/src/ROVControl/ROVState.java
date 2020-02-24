package ROVControl;

/**
 * A mutable representation of the state of an ROV.
 */
public class ROVState {
    private float verticalSpeed;
    private float forwardSpeed;
    private float rightSpeed;
    private float rotationSpeed;
    private Boolean[] lights;

    /**
     * Constructs a new, default ROVState.
     * @modifies this
     * @effects this is a new ROVState with all lights set to off and speed of 0.
     */
    public ROVState() {}

    /**
     * Makes an independent copy of this ROVState.
     * @return a copy of this ROVState.
     */
    public ROVState copy() {
        ROVState state = new ROVState();
        // Notice that we can get private fields inside the ROVState that we made.
        state.verticalSpeed = verticalSpeed;
        state.forwardSpeed = forwardSpeed;
        state.rightSpeed = rightSpeed;
        state.rotationSpeed = rotationSpeed;
        // TODO: Implement lights copying
        return state;
    }

    /**
     * Sets the horizontal Speed components of the ROV State.
     * @spec.requires forwardSpeed and rightSpeed must be between [-1, 1] (inclusive).
     */
    public void setHorizontalSpeed(float forwardSpeed, float rightSpeed) {
        if (forwardSpeed < -1 && forwardSpeed > 1) {
            throw new IllegalArgumentException("Forward speed must be between [-1, 1].");
        }
        if (rightSpeed < -1 && rightSpeed > 1) {
            throw new IllegalArgumentException("Right speed must be between [-1, 1].");
        }

        this.forwardSpeed = forwardSpeed;
        this.rightSpeed = rightSpeed;
    }

    /**
     *
     */
    public float getForwardSpeed() {
        throw new IllegalArgumentException("Not yet implemented.");
    }
}
