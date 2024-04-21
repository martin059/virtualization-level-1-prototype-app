/**
 * Represents a navigation object with a title and a href.
 */
export class NavObject {
    /**
     * Creates a new NavObject instance.
     * @param title - The title of the navigation object.
     * @param href - The href of the navigation object.
     */
    constructor(public title: string, public href: string) {}

    /**
     * Gets the lowercase value of the title.
     */
    get label(): string {
        return this.title.toLowerCase();
    }
}